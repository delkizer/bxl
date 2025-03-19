import jwt
import traceback
import custom_exception
import json

from class_config.class_env import Config
from class_config.class_db import ConfigDB
from class_lib.api.base_model import UserCreate
from class_lib.local_utils import utils
from define.define_code import DefineCode

from datetime import datetime, timedelta, timezone
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError
from passlib.context import CryptContext

class Auth:
    def __init__(self, logger):
        self.config = Config()
        self.class_name = __name__.split('.')[-1].replace('class_', '')
        self.logger = logger
        self.define_code = DefineCode()
        self.utils = utils.Utils(self.logger)
        self.config = Config()
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

    def is_jwt_verify(self, token: str):
        with open(self.jwt_public_key, "r") as f:
            public_key = f.read()

        try:
            decoded_token = jwt.decode(
                token,
                public_key,
                algorithms=[self.define_code.JWT_ALGORITHM]
            )
            return decoded_token

        except jwt.ExpiredSignatureError as e:
            self.logger.error(f"[is_jwt_verify] Token expired: {token}\n{traceback.format_exc()}")
            raise custom_exception.ExpiredTokenError("Token expired") from e

        except jwt.InvalidSignatureError as e:
            self.logger.error(f"[is_jwt_verify] Invalid signature: {token}\n{traceback.format_exc()}")
            raise custom_exception.InvalidTokenError("Invalid signature") from e

        except Exception as e:
            self.logger.error(f"[is_jwt_verify] Exception: {e}\n{traceback.format_exc()}")
            raise custom_exception.BaseProjectError("Invalid token", 401) from e

    def get_redirect_uri(self):
        try:
            hostname = self.utils.get_hostname().lower()
            #self.logger.info(f"[get_redirect_uri] hostname: {hostname}")

            # 예시 로직. 팀 상황에 맞춰 수정
            if 'win' in hostname:
                # 로컬 개발(Windows) 가정
                return "http://localhost:5173" + self.config.google_redirect_path
            else:
                return self.config.google_redirect_url + self.config.google_redirect_path
        except Exception as e:
            self.logger.error(f"[get_redirect_uri] Exception: {e}\n{traceback.format_exc()}")
            raise custom_exception.BaseProjectError("server check error", 500) from e

    def get_front_uri(self):
        hostname = self.utils.get_hostname().lower()

        # 예시 로직. 팀 상황에 맞춰 수정
        if 'win' in hostname:
            # 로컬 개발(Windows) 가정
            return "http://localhost:8001"
        else:
            return self.config.auth_front_url

    def insert_cms_admins_01(self, email, providers, token_data, custom_jwt):
        query = text("""
            INSERT INTO auth.cms_admins (
                email, providers, token, jwt
            ) VALUES (
                :email, :providers, :token, :jwt
            )
            ON CONFLICT (email)
            DO UPDATE SET providers = EXCLUDED.providers,
                          token = EXCLUDED.token,
                          jwt = EXCLUDED.jwt
            RETURNING *
        """)
        result_dict:dict = {}
        session = self.astm_admin_session_factory()

        try:
            if session is None:
                self.logger.error("astm_admin_session_factory() returned None (session is None).")
                raise RuntimeError("astm_admin_session_factory() returned None (session is None).")

            token_as_str = json.dumps(token_data) if isinstance(token_data, dict) else str(token_data)

            result_dict = {
                "email": email,
                "providers": providers,
                "token": token_as_str,
                "jwt": custom_jwt
            }

            session.execute(query, result_dict)
            session.commit()
            self.logger.info(f"Inserted 1 row into cms_admins.{result_dict}")

        except IntegrityError as e:
            self.logger.error("Unique constraint or foreign key error occurred", exc_info=True)
            session.rollback()
            raise e
        except Exception as e:
            self.logger.error(f"Error inserting into insert_cms_admins_01: {result_dict}^{e}", traceback.format_exc())
            raise e
        finally:
            if session is not None:
                session.close()

    def get_cms_admins_01(self, jwt):
        query = text("""
            SELECT token, providers, email FROM auth.cms_admins WHERE jwt = :jwt 
        """)
        try:
            session = self.astm_admin_session_factory()
            result = session.execute(query, {'jwt': jwt}).mappings().all()
            session.close()

            if result:
                jwt_list = [dict(row) for row in result]
                self.logger.info(f"get get_cms_admins_01 list with jwt info: {jwt_list}")
                return jwt_list
            return []
        except Exception as e:
            self.logger.error(f"Error get_cms_admins_01 querying the database for game id: {e}")
            return []

    def get_jwt_verify(self,credentials: HTTPAuthorizationCredentials):
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid",
            )
        custom_jwt = credentials.credentials
        self.logger.info(f"[get_jwt_verify] custom_jwt: {custom_jwt}")

        try:
            # 1) 공개키 로딩
            with open(self.jwt_public_key, "r") as f:
                public_key_content = f.read()

            # 2) JWT 디코딩
            jwt.decode(custom_jwt, public_key_content, algorithms=["RS256"])

            try:
                token_list = self.get_cms_admins_01(custom_jwt)
                if not token_list:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="JWT token not found in DB"
                    )
            except Exception as e:
                self.logger.error(f"[verify_jwt_token_or_raise] DB Exception Exception: {e}", traceback.format_exc())
                raise HTTPException(status_code=500, detail="Internal Server Error")

            return token_list

        except ExpiredSignatureError:
            self.logger.error("[get_jwt_verify] ExpiredSignatureError", traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Expired JWT token"
            )
        except InvalidSignatureError:
            self.logger.error("[get_jwt_verify] InvalidSignatureError", traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid signature"
            )
        except InvalidTokenError as e:
            self.logger.error(f"[get_jwt_verify] InvalidTokenError: {e}", traceback.format_exc())
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Invalid token: {e}"
            )
        except Exception as e:
            self.logger.error(f"[get_jwt_verify] Exception: {e}", traceback.format_exc())
            raise HTTPException(status_code=500, detail="Internal Server Error")

