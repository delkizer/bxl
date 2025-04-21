from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .router import router

def create_app() -> FastAPI:
    app = FastAPI(
        title="BXL",
        description="BXL 베드민턴 프로젝트 ",
        version="0.0.1",
        docs_url="/api/docs",  # Swagger UI 라우트
        redoc_url="/api/redoc",  # Redoc 라우트 (원하면 삭제 가능)
        openapi_url="/api/openapi.json",  # OpenAPI JSON
        swagger_ui_parameters={
            "withCredentials": True,
            "persistAuthorization": True,
        },
    )

    # 라우터 등록
    app.include_router(router)

    # CORS를 허용할 도메인(혹은 포트) 목록
    origins = [
        "http://localhost:5173",
        "http://localhost:7001",
        "http://13.125.50.113:8080",
        "https://bxl-dev.delkizer.com"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # or ["*"] 로 모든 도메인 허용
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.middleware("http")
    async def debug_host(request, call_next):
        print("▶︎ HOST:", request.headers.get("host"))
        return await call_next(request)

    return app
