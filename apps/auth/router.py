from fastapi import APIRouter, Depends, Request, HTTPException, status
from fastapi.responses import JSONResponse

from class_config.class_db import ConfigDB
from class_lib.api.auth import Auth
from class_config.class_env import Config
from class_config.class_log import ConfigLogger
from class_lib.api.base_model import UserLogin, UserCreate, UserInfo

config  = Config()
logger  = ConfigLogger('http_log', 365).get_logger('auth')
auth    = Auth(logger)
db_config = ConfigDB()

router = APIRouter(prefix="/api")

# 로그인 API (Swagger 연동 포함)
@router.post("/login", tags=["Auth"])
async def user_login(user: UserLogin):
    """
    - 유저 로그인 API
    """

    role = "admin"
    try:
        logger.info(f"Login attempt: {user.email}")

        auth.authenticate_user(user.email, user.password, role)
        access_token = auth.get_jwt_token(user.email, config.jwt_sub)

        refresh_token = auth.create_refresh_token(user.email, config.jwt_sub)
        auth.save_refresh_token_to_db(user.email, refresh_token)

        response = JSONResponse(content={
            "msg": "login successful",
        })

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            #secure=config.set_cookie_secret,  # HTTPS 환경이라면 True
            #samesite=config.set_cookie_samesite,
            secure=True,
            samesite="none",
            path="/",
            max_age=60 * 60 * 24  # 1일 등 원하는 유효기간
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            #secure=config.set_cookie_secret,
            #samesite=config.set_cookie_samesite,
            secure=True,
            samesite="none",
            path="/",
            max_age=60 * 60 * 24 * 8
        )

        return response

    except HTTPException as http_exc:
        # authenticate_user에서 발생한 HTTPException을 그대로 전달
        logger.warning(f"Authentication failed for {user.email}: {http_exc.detail}")
        raise http_exc

    except Exception as exc:
        # 기타 예외 처리
        logger.error(f"Internal server error during authentication: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/create_user", tags=["Auth"])
async def create_user(user: UserCreate):
    """
    - 유저 신규 등록 API
    """
    try:
        auth.create_user(user)
        return {"message": "User created successfully"}

    except HTTPException as http_exc:
        logger.warning(f"User creation failed for {user.email}: {http_exc.detail}")
        raise http_exc

    except Exception as exc:
        logger.error(f"Internal server error during user creation: {exc}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/userinfo", tags=["Auth"])
async def get_userinfo( user: UserInfo = Depends(auth.get_current_user)):
    """
    현재 로그인한 사용자 정보
    """
    return user

@router.post("/refresh_token", tags=["Auth"])
async def refresh_token(request: Request):
    """
    사용자의 access 토큰을 재생성
    """
    refresh_token = request.cookies.get("refresh_token")
    logger.info(f"refresh_token:{refresh_token}")

    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not provided")

    try:
        payload = auth.verify_refresh_token(refresh_token)
        email = payload.get("email")

        new_access_token = auth.get_jwt_token(email, config.jwt_sub)
        response = JSONResponse({"msg": "access token refreshed"})
        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=config.set_cookie_secret,  # HTTPS 환경이라면 True
            samesite=config.set_cookie_samesite,
            path="/",
            max_age=60 * 60 * 24  # 1일 등 원하는 유효기간
        )

        return response
    except HTTPException as e:
        response = JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": e})
        response.delete_cookie("refresh_token")
        response.delete_cookie("access_token")
        return response