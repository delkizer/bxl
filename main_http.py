from fastapi import FastAPI, Path, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from class_config.class_env import Config
from class_config.class_log import ConfigLogger
from class_config.class_db import ConfigDB
from class_config.class_define import Define

from class_lib.api.base_model import UserLogin, UserCreate
from class_lib.api.auth import Auth
from define.define_code import DefineCode

# 기본 클래스 설정
config = Config()
config_logger = ConfigLogger('http_log', 365)
logger = config_logger.get_logger('fastapi')
define = Define()
define_code = DefineCode()
db_config = ConfigDB()

auth = Auth( logger )

# title, description 등 OpenAPI 문서용 설정을 줄 수 있음
app = FastAPI(
    title="BXL",
    description="BXL 베드민턴 프로젝트 ",
    version="0.0.1",
    docs_url="/api/docs",               # Swagger UI 라우트
    redoc_url="/api/redoc",             # Redoc 라우트 (원하면 삭제 가능)
    openapi_url="/api/openapi.json",    # OpenAPI JSON
)

# CORS를 허용할 도메인(혹은 포트) 목록
origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # or ["*"] 로 모든 도메인 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/hello/{name}", tags=["Sample"])
async def say_hello(
        name: str = Path(..., description="사용자 이름 (경로 파라미터)")
):
    """
    - path parameter `name`을 받아서 "Hello {name}"을 반환
    """
    return {"message": f"Hello {name}"}

# 로그인 API (Swagger 연동 포함)
@app.post("/api/login", tags=["Auth"])
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
            secure=config.set_cookie_secret,  # HTTPS 환경이라면 True
            samesite="none",  # 또는 lax / strict
            path="/",
            max_age=60 * 60 * 24  # 1일 등 원하는 유효기간
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=config.set_cookie_secret,
            samesite="none",
            path="/",
            max_age=60 * 60 * 24 * 8
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

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

@app.post("/api/create_user", tags=["User Management"])
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



