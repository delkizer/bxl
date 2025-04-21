from fastapi import FastAPI
from apps.bxl.router import router
from apps.auth.router import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="BXL",
        description="BXL 베드민턴 프로젝트 ",
        version="0.0.1",
#        docs_url="/bwf_api/docs",  # Swagger UI 라우트
#        redoc_url="/bwf_api/redoc",  # Redoc 라우트 (원하면 삭제 가능)
#        openapi_url="/bwf_api/openapi.json",  # OpenAPI JSON
        docs_url=None,
        openapi_url=None,
        swagger_ui_parameters={
            "withCredentials": True,
            "persistAuthorization": True,
        },
    )

    # 라우터 등록
    app.include_router(router)
    app.include_router(auth_router)

    '''
    @app.middleware("http")
    async def debug_host(request, call_next):
        print("▶︎ HOST:", request.headers.get("host"))
        return await call_next(request)
    '''

    return app
