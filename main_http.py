from fastapi import FastAPI
from starlette.routing import Host
from apps.bxl.app import create_app as create_bxl_app

bxl_app = create_bxl_app()

routes = (
    Host("localhost", app=bxl_app, name="bxl-local"),
    Host("127.0.0.1", app=bxl_app, name="bxl-loopback"),
    Host("13.125.50.113", app=bxl_app, name="bxl-ip"),
    Host("bxl-dev.delkizer.com", app=bxl_app, name="bxl-dev"),
)

app = FastAPI(routes=routes)
