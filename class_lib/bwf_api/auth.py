import jwt
import traceback
import custom_exception

from class_config.class_env import Config
from class_config.class_db import ConfigDB
from class_lib.bwf_api.base_model import UserCreate
from class_lib.local_utils import utils
from define.define_code import DefineCode

from datetime import datetime, timedelta, timezone
from sqlalchemy.sql import text
from fastapi import HTTPException, status, Request
from passlib.context import CryptContext
from jose import jwt, JWTError

class Auth:
    def __init__(self, logger):
        self.config = Config()
        self.class_name = __name__.split('.')[-1].replace('class_', '')
        self.logger = logger
        self.define_code = DefineCode()
        self.utils = utils.Utils(self.logger)
        self.db = ConfigDB()
        self.bxl_session_factory = self.db.get_bxl_session_factory(self.config)

        self.jwt_private_key = self.config.jwt_key_path + "/private_key.pem"
        self.jwt_public_key = self.config.jwt_key_path + "/public_key.pem"

        # 비밀번호 암호화 컨텍스트
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # 사용자 인증
    def authenticate_user(self, email: str, password: str, role: str):
        session = self.bxl_session_factory()
        try:
            query = text("""
                SELECT password_hash, role, is_active
                  FROM bxl.admin_users
                 WHERE email = :email  
            """)
            result = session.execute(query, {'email': email}).mappings().all()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user_info = result[0]
            self.logger.info(f"DB hash: {user_info['password_hash']}")
            hashed_password = self.pwd_context.hash(password)
            self.logger.info(f"hashed_password={hashed_password}")

            if not self.pwd_context.verify(password, user_info['password_hash']):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if user_info['role'] != role:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect role",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            if not user_info['is_active']:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User is not activated",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return True

        except HTTPException as http_exc:
            # HTTPException을 그대로 재전달
            raise http_exc

        except Exception as e:
            self.logger.error(f"Error authenticate_user querying the database for email={email}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
                headers={"WWW-Authenticate": "Bearer"},
            )
        finally:
            session.close()

    def create_user(self, user: UserCreate):
        password_hash = self.pwd_context.hash(user.password)

        session = self.bxl_session_factory()
        try:
            query = text("""
                         INSERT INTO bxl.admin_users (email, password_hash, full_name, role, is_active)
                         VALUES (:email, :password_hash, :full_name, :role, :is_active)
                         """)
            session.execute(query, {
                'email': user.email,
                'password_hash': password_hash,
                'full_name':user.full_name,
                'role': user.role,
                'is_active':user.is_active
            })
            session.commit()
            return {"message": "User created"}

        except Exception as e:
            session.rollback()
            self.logger.error(f"User creation failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            session.close()

    def get_jwt_token(self, email:str, sub: str):
        payload = {
            "email": email,
            "type": "access",
            "sub": sub,
            "exp": datetime.now(timezone.utc) + timedelta(hours=int(self.config.jwt_expire_minutes)),
            "iat": datetime.now(timezone.utc)
        }

        try:
            with open(self.jwt_private_key, "r") as f:
                private_key = f.read()

            token = jwt.encode(
                payload,
                private_key,
                algorithm=self.define_code.JWT_ALGORITHM
            )
            return token

        except FileNotFoundError as e:
            # 키 파일이 없거나 경로가 잘못된 경우
            self.logger.error(f"[get_jwt_token] Private key file not found: {e}\n{traceback.format_exc()}")
            raise custom_exception.PrivateKeyNotFoundError(e)

        except Exception as e:
            # 기타 예외
            self.logger.error(f"[get_jwt_token] Exception: {e}\n{traceback.format_exc()}")
            raise custom_exception.BaseProjectError("Internal error", 500) from e

    def create_refresh_token(self, email: str, sub: str, expires_days: int = 7):
        payload = {
            "email": email,
            "type": "refresh",
            "sub": sub,
            "exp": datetime.now(timezone.utc) + timedelta(hours=expires_days),
            "iat": datetime.now(timezone.utc)
        }
        try:
            with open(self.jwt_private_key, "r") as f:
                private_key = f.read()

            refresh_token = jwt.encode(
                payload,
                private_key,
                algorithm=self.define_code.JWT_ALGORITHM
            )

            return refresh_token

        except FileNotFoundError as e:
            # 키 파일이 없거나 경로가 잘못된 경우
            self.logger.error(f"[create_refresh_token] Private key file not found: {e}\n{traceback.format_exc()}")
            raise custom_exception.PrivateKeyNotFoundError(e)

        except Exception as e:
            # 기타 예외
            self.logger.error(f"[create_refresh_token] Exception: {e}\n{traceback.format_exc()}")
            raise custom_exception.BaseProjectError("Internal error", 500) from e

    def save_refresh_token_to_db(self, email, refresh_token, expires_days=7):
        session = self.bxl_session_factory()
        try:
            query = text("""
            UPDATE bxl.admin_users
               SET refresh_token = :refresh_token, 
                   token_expire_at = :token_expire_at
             WHERE email = :email 
                         """)
            session.execute(query, {
                'email': email,
                'refresh_token': refresh_token,
                'token_expire_at': datetime.now(timezone.utc) + timedelta(days=expires_days)
            })
            session.commit()
            return True

        except Exception as e:
            session.rollback()
            self.logger.error(f"Saving refresh token failed for email={email}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            session.close()

    def get_current_user(self, request: Request):
        """
        FastAPI 의존성 - 쿠키에서 access_token을 꺼내 검증
        """
        token = request.cookies.get("access_token")
        #self.logger.debug(f"[get_current_user] token: {token}")
        if not token:
            raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="No access token" )
        payload = self.verify_access_token(token)
        email = payload.get("email")
        if not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload does not contain an email/sub."
            )

        user = self.find_user_in_db_by_email(email)
        return user

    def verify_access_token(self, token: str):
        """
        JWT Access Token 검증: 서명 & 만료 확인
        """
        try:
            with open(self.jwt_public_key, "r") as f:
                public_key = f.read()

            payload = jwt.decode(token, public_key, algorithms=[self.define_code.JWT_ALGORITHM])
            return payload
        except JWTError as e:
            # 서명 불일치, 만료, 형식오류 등
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token error: {str(e)}",
            )
        except Exception as e:
            self.logger.error(f"[verify_access_token] Exception: {e}\n{traceback.format_exc()}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def find_user_in_db_by_email(self, email: str):
        session = self.bxl_session_factory()
        try:
            query = text("""
                SELECT email, role, is_active, full_name FROM bxl.admin_users WHERE email = :email
            """)
            result = session.execute(query, {'email': email}).mappings().all()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND
                    , detail=f"User with email '{email}' not found."
                )
            return result

        except Exception as e:
            self.logger.error(f"[find_user_in_db_by_email] Exception: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal database error."
            )

        finally:
            session.close()

    def verify_refresh_token(self, token: str):
        session = None
        try:
            with open(self.jwt_public_key, "r") as f:
                public_key = f.read()

            payload = jwt.decode(token, public_key, algorithms=[self.define_code.JWT_ALGORITHM])
            if payload.get("type") != "refresh":
                raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token" )

            session = self.bxl_session_factory()
            query = text("""
                         SELECT token_expire_at
                         FROM bxl.admin_users
                         WHERE refresh_token = :token
                         """)
            result = session.execute(query, {'token': token}).mappings().all()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail = "Refresh token not found or invalid"
                )

            # DB의 만료시간과 JWT의 exp가 일치하는지 추가로 비교
            db_expire = result[0]["token_expire_at"]
            token_exp = datetime.fromtimestamp(payload['exp'], timezone.utc)

            if datetime.now(timezone.utc) > db_expire:
                raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired" )

            if datetime.now(timezone.utc) > token_exp:
                raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token JWT expired" )

            return payload

        except JWTError as e:
            self.logger.error(f"[verify_refresh_token] Exception: {e}", exc_info=True)
            raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

        except Exception as e:
            self.logger.error(f"[verify_refresh_token] Exception: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal database error."
            )

        finally:
            if session is not None:
                session.close()

