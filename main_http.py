from fastapi import FastAPI
from starlette.routing import Host
from fastapi.middleware.cors import CORSMiddleware
from apps.bxl.app import create_app as create_bxl_app
from apps.auth.app import create_auth_app
from fastapi.openapi.utils import get_openapi

auth_app = create_auth_app()
bxl_app  = create_bxl_app()

def custom_openapi():
    root_schema = get_openapi(
        title="BWF/BXL API",
        version="0.0.1",
        routes=root.routes,
    )

    # ── 서브앱 스키마 병합 ─────────────────────────────
    for sub in (auth_app, bxl_app):
        sub_schema = sub.openapi()
        # paths
        for path, item in sub_schema["paths"].items():
            root_schema["paths"][path] = item
        # components
        for comp, obj in sub_schema.get("components", {}).items():
            root_schema.setdefault("components", {}).setdefault(comp, {}).update(obj)

    return root_schema
root = FastAPI(
    title="BWF/BXL API",
    docs_url="/bwf_api/docs",
    openapi_url="/bwf_api/openapi.json",
)
root.openapi = custom_openapi
# 공통 CORS 추가
root.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https:\/\/.*\.delkizer\.com$|http:\/\/localhost:\d+$|http:\/\/127\.0\.0\.1:\d+$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서브앱 생성
root.mount("/auth", create_auth_app())
root.router.routes.extend([
    Host("localhost", app=bxl_app, name="bxl-local"),
    Host("127.0.0.1", app=bxl_app, name="bxl-loop"),
    Host("bxl-dev.delkizer.com", app=create_bxl_app(), name="bxl-dev"),
])

app = root
