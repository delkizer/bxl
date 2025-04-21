import uuid
from typing import Optional, List

from fastapi import APIRouter
from fastapi import Path, Depends, Request, Query, Body

from class_config.class_db import ConfigDB
from class_config.class_define import Define
from class_config.class_env import Config
from class_config.class_log import ConfigLogger
from class_lib.api.tour import Tour
from class_lib.api.coder import Coder
from class_lib.api.team import Team
from class_lib.api.officials import Officials
from define.define_code import DefineCode
from class_lib.api.auth import Auth
from class_lib.api.base_model import UserInfo, TourInfo, TeamAndPlayerInfo, TieInfo, OfficialInfo, GameOfficialInfo \
    , OfficialSearch

router = APIRouter(prefix="/api")

# 기본 클래스 설정
config = Config()
config_logger = ConfigLogger('http_log', 365)
logger = config_logger.get_logger('auth')
define = Define()
define_code = DefineCode()
db_config = ConfigDB()

coder = Coder( logger )
tour = Tour( logger )
team = Team( logger )
auth    = Auth(logger)
officials = Officials( logger )

@router.get("/hello/{name}", tags=["Sample"])
async def say_hello(
        name: str = Path(..., description="사용자 이름 (경로 파라미터)")
):
    """
    - path parameter `name`을 받아서 "Hello {name}"을 반환
    """
    return {"message": f"Hello {name}"}



@router.get("/gamelist", tags=["Coder"])
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

@router.get("/matchtype/list", tags=["Tournament"])
async def get_matchtype_list(
        request: Request,
):
    result = tour.get_matchtype_list()

    return result


@router.post("/tourpage", tags=["Tournament"])
async def create_tourpage(
        request: Request,
        tour_info: TourInfo,
):
    """

    """
    result = tour.create_tour(tour_info)
    return result

@router.delete("/tourpage", tags=["Tournament"])
async def delete_tourpage(
        request: Request,
        tournament_uuid: uuid.UUID = Body(..., embed=True)
):
    result = tour.delete_tour(tournament_uuid)
    return result

@router.get("/nationlist", tags=["Tournament"])
async def get_nationlist(
        request: Request,
):
    """
    :param request: None
    :return: 국가코드 : 국가이름 리스트
    """
    result = tour.nation_list()
    return result



@router.get("/tourlist", tags=["Tournament"])
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

@router.post("/teampage", tags=["Team"])
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

@router.get("/teamlist", tags=["Team"])
async def get_teamlist(
        request: Request,
):
    """
    :param request:
    :return: 각각의 BXL 대회에 참가한 팀 리스트 노출
    """
    result = team.get_team_list()
    return result

@router.get("/teams/{team_code}/players", tags=["Team"])
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

@router.get("/tiepage", tags=["Coder"])
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

@router.post("/tiepage", tags=["Coder"])
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

@router.post("/tiemodify", tags=["Coder"])
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

@router.get("/officials", tags=["Official"])
async def get_officials(
        request: Request,
        official_info: Optional[OfficialSearch] = None,
):
    """
    :param request:
    :return:
    """
    result = officials.get_officials( official_info )
    return result

@router.post("/officials", tags=["Official"])
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

@router.put("/officials", tags=["Official"])
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

@router.delete("/officials", tags=["Official"])
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

@router.post("/gameofficials", tags=["Official"])
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

@router.delete("/gameofficials", tags=["Official"])
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

@router.get("/gameuuids", tags=["GOfficial"])
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

@router.get("/gameties", tags=["GOfficial"])
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

@router.get("/gameofficials", tags=["Official"])
async def get_gameofficials(
        request: Request,
        tournament_uuid: Optional[uuid.UUID] = Query(None, description="토너먼트 UUID"),
        tie_no: Optional[int] = Query(None, description="토너먼트에 해당하는 tie no"),
        match_no: Optional[int] = Query(None, description="토너먼트에 해당하는 match no"),
        game_uuid: Optional[uuid.UUID] = Query(None, description="토너먼트에 match 당 해당하는 game no"),
):

    result = officials.get_gameofficials(tournament_uuid, tie_no, match_no, game_uuid)
    return result

@router.get("/coderinfo", tags=["Coder"])
async def get_coderinfo(
        request: Request,
        tournament_uuid: Optional[uuid.UUID] = Query(None, description="토너먼트 UUID"),
        tie_no: Optional[int] = Query(None, description="토너먼트에 해당하는 tie no"),
):
    result = coder.get_coderinfo(tournament_uuid, tie_no)
    return result