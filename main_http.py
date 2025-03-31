import uuid

from typing import Optional, List

from fastapi import FastAPI, Path, HTTPException, status, Depends, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from class_config.class_env import Config
from class_config.class_log import ConfigLogger
from class_config.class_db import ConfigDB
from class_config.class_define import Define

from class_lib.api.base_model import UserLogin, UserCreate, UserInfo, TourInfo, TeamAndPlayerInfo, TieInfo, \
    OfficialInfo, GameOfficialInfo
from class_lib.api.auth import Auth
from class_lib.api.coder import Coder
from class_lib.api.team import Team
from class_lib.api.tour import Tour
from class_lib.api.officials import Officials
from define.define_code import DefineCode

# 기본 클래스 설정
config = Config()
config_logger = ConfigLogger('http_log', 365)
logger = config_logger.get_logger('auth')
define = Define()
define_code = DefineCode()
db_config = ConfigDB()
auth = Auth( logger )
coder = Coder( logger )
tour = Tour( logger )
team = Team( logger )
officials = Officials( logger )

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
            samesite=config.set_cookie_samesite,
            path="/",
            max_age=60 * 60 * 24  # 1일 등 원하는 유효기간
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=config.set_cookie_secret,
            samesite=config.set_cookie_samesite,
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

@app.post("/api/create_user", tags=["Auth"])
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

@app.get("/api/userinfo", tags=["Auth"])
async def get_userinfo( user: UserInfo = Depends(auth.get_current_user)):
    """
    현재 로그인한 사용자 정보
    """
    return user

@app.post("/api/refresh_token", tags=["Auth"])
async def refresh_token(request: Request):
    """
    사용자의 access 토큰을 재생성
    """
    refresh_token = request.cookies.get("refresh_token")

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

@app.get("/api/gamelist", tags=["Coder"])
async def get_gamelist(
        request: Request,
        game_date: Optional[str] = Query(None, description="필요하다면 게임 날짜 (YYYY-MM-DD)"),
        tournament_uuid: Optional[uuid.UUID] = Query(None, description="토너먼트 UUID"),
        user : UserInfo = Depends(auth.get_current_user),
):
    """
    - **tournament_uuid**: 필수 Path Param
    - **game_date**: 필수 Path Param
    """
    result = coder.get_game_list(game_date, tournament_uuid)

    return result

@app.get("/api/matchtype/list", tags=["Tournament"])
async def get_matchtype_list(
        request: Request,
):
    result = tour.get_matchtype_list()

    return result


@app.post("/api/tourpage", tags=["Tournament"])
async def create_tourpage(
        request: Request,
        tour_info: TourInfo,
):
    """

    """
    result = tour.create_tour(tour_info)
    return result

@app.get("/api/nationlist", tags=["Tournament"])
async def get_nationlist(
        request: Request,
):
    """
    :param request: None
    :return: 국가코드 : 국가이름 리스트
    """
    result = tour.nation_list()
    return result

@app.get("/api/tourlist", tags=["Tournament"])
async def get_tourlist(
        request: Request,
        tournament_uuid: Optional[uuid.UUID] = Query(None, description="토너먼트 UUID"),
):
    """
    :param request: None
    :return: 현재 BXL에 해당하는 대뢰 리스트 리턴
    """
    result = tour.tour_list(tournament_uuid)
    return result

@app.post("/api/teampage", tags=["Team"])
async def get_teampage(
        request: Request,
        team_player_info: TeamAndPlayerInfo,
):
    """
    :param request:
    :return: 현재 BXL 대회에 참여한 팀 구성
    """
    result = team.create_team_and_player(team_player_info)
    return result

@app.get("/api/teamlist", tags=["Team"])
async def get_teamlist(
        request: Request,
):
    """
    :param request:
    :return: 각각의 BXL 대회에 참가한 팀 리스트 노출
    """
    result = team.get_team_list()
    return result

@app.get("/api/teams/{team_code}/players", tags=["Team"])
async def get_playerlist(
        request: Request,
        team_code: str = Path(..., description="선수가 속한 팀 코드")
):
    """
    :param request:
    :return: 각 팀에 속한 선수리스트
    """
    result = team.get_player_list(team_code)
    return result

@app.get("/api/tiepage", tags=["Coder"])
async def get_tielist(
        request: Request,
        tournament_uuid: Optional[uuid.UUID] = Query(None, description="토너먼트 UUID"),
        tie_no: Optional[int] = Query(None, description="토너먼트에 해당하는 tie no"),
        game_date: Optional[str] = Query(None, description="tie가 벌어지는 날자"),
):
    """
    :param request:
    :return: tai에 해당하는 팀과 정보 리스트 전체 전달
    """
    result = coder.get_tie_page(tournament_uuid, tie_no, game_date)
    return result

@app.post("/api/tiepage", tags=["Coder"])
async def get_tiepage(
        request: Request,
        tie_info: TieInfo,
):
    """
    :param request: 
    :return: 
    """
    result = coder.create_tie(tie_info)
    return result

@app.post("/api/tiemodify", tags=["Coder"])
async def get_tiemodify(
        request: Request,
        tie_info: TieInfo,
):
    """
    :param request:
    :param tie_info:
    :return:
    """
    result = coder.modify_tie(tie_info)
    return result

@app.get("/api/officials", tags=["Officail"])
async def get_officials(
        request: Request,
        #official_info: OfficialInfo = Depends(officials.official_info_query),
):
    """
    :param request:
    :return:
    """
    #official_info: OfficialInfo = OfficialInfo(  )
    result = officials.get_officials(  )
    return result

@app.post("/api/officials", tags=["Official"])
async def get_officials(
        request: Request,
        official_list: List[OfficialInfo],
):
    """
    :param request:
    :param official_list:
    :return:
    """

    result = officials.post_officials(official_list)
    return result

@app.put("/api/officials", tags=["Official"])
async def put_officials(
        request: Request,
        official_list: List[OfficialInfo],
):
    """
    :param request:
    :param official_list:
    :return:
    """
    result = officials.put_officials(official_list)
    return result

@app.delete("/api/officials", tags=["Official"])
async def delete_officials(
        request: Request,
        official_list: List[OfficialInfo],
):
    """
    :param request:
    :param official_list:
    :return:
    """
    result = officials.delete_officials(official_list)
    return result

@app.post("/api/gameofficials", tags=["Official"])
async def post_gameofficials(
        request: Request,
        gameofficial_info: List[GameOfficialInfo],
):
    """
    :param request:
    :param gameofficial_info:
    :return:
    """
    result = officials.post_gameofficial(gameofficial_info)
    return result

@app.put("/api/gameofficials", tags=["Official"])
async def put_gameofficials(
        request: Request,
        gameofficial_info: List[GameOfficialInfo],
):
    """
    :param request:
    :param gameofficial_info:
    :return:
    """
    result = officials.put_gameofficials(gameofficial_info)
    return result

@app.delete("/api/gameofficials", tags=["Official"])
async def delete_gameofficials(
        request: Request,
        gameofficial_info: List[GameOfficialInfo],
):
    """
    :param request:
    :param gameofficial_info:
    :return:
    """
    result = officials.delete_gameofficials(gameofficial_info)
    return result

@app.get("/api/gameuuids", tags=["GOfficial"])
async def get_gameuuids(
        request: Request,
        tournament_uuid: Optional[uuid.UUID] = Query(None, description="토너먼트 UUID"),
        tie_no: Optional[int] = Query(None, description="토너먼트에 해당하는 tie no"),
        match_no: Optional[int] = Query(None, description="토너먼트에 해당하는 match no"),
):
    """
    :param request:
    :param tournament_uuid:
    :param tie_no:
    :param match_no:
    :return:
    """
    result = officials.get_gameuuids(tournament_uuid, tie_no, match_no)
    return result

@app.get("/api/gameties", tags=["GOfficial"])
async def get_gameties(
        request: Request,
        tournament_uuid: Optional[uuid.UUID] = Query(None, description="토너먼트 UUID"),
):
    """
    :param request:
    :param tournament_uuid:
    :return:
    """
    result = officials.get_gameties(tournament_uuid)
    return result
