"""
Auth 서브앱 ‑ SSO 전용 FastAPI 인스턴스
--------------------------------------
* 로그인, 토큰 재발급, 로그아웃 엔드포인트만 포함
* domain=".delkizer.com" 쿠키 설정으로 모든 서브도메인 공유
* 필요하면 main_http.py 에서 **/auth** 경로 또는 별도 Host 로 mount
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.auth.router import router as auth_router
from class_config.class_env import Config

cfg = Config()

def create_auth_app() -> FastAPI:
    app = FastAPI(
        title="Auth Service (SSO)",
        version="0.0.1",
#        docs_url="/bwf_api/docs",
#        openapi_url="/openapi.json",
        docs_url=None,
        openapi_url=None,
        swagger_ui_parameters={
            "withCredentials": True,
            "persistAuthorization": True,
        },
    )

    # ─────────────── 공통 CORS (필요 시) ───────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https:\/\/.*\.delkizer\.com$",
        allow_credentials=True,
        allow_methods=["POST", "GET"],
        allow_headers=["*"],
    )

    # ─────────────── 인증 라우터 등록 ───────────────
    app.include_router(auth_router)

    return app
