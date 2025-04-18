import uuid
from typing import Optional, List

from fastapi import Query
from pydantic import BaseModel, Field

class UserLogin(BaseModel):
    email: str = Field(..., example="user@example.com")
    password: str = Field(..., example="your_password")

class UserCreate(BaseModel):
    email: str = Field(..., example="user@example.com")
    password: str = Field(..., example="your_password")
    full_name: str = Field(..., example="test user")
    role: str = Field(..., example="admin")
    is_active: bool = Field(..., example=True)

class UserInfo(BaseModel):
    email: str = Field(..., example="user@example.com")
    full_name: str = Field(..., example="test user")
    role: str = Field(..., example="admin")

class TokenExchangeResponse(BaseModel):
    message: str = Field(..., example="Token exchange success")
    access_token: str = Field(..., example="ya29.a0AfH6SM...")
    refresh_token: str = Field(..., example="1//0gBxxxR...")
    expires_in: int = Field(..., example=3599)
    id_token: str = Field(..., example="eyJhbGciOiJSUzI1N...")
    custom_jwt: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ey...")
    # 필요에 따라 더 많은 필드를 추가

class TokenExchangeError(BaseModel):
    error: str = Field(..., example="No code in callback")
    detail: str = Field(None, example="Token exchange failed")

class GetSessionInfo(BaseModel):
    HomeTeam_Name: Optional[str]
    AwayTeam_Name: Optional[str]
    GameReference: Optional[str]
    Field_Name: Optional[str]
    Field_ShortName: Optional[str]
    League_ShortName: Optional[str]
    SessionStartedLocal: Optional[str]

class TourInfo(BaseModel):
    tournament_uuid: Optional[uuid.UUID] = None
    tournament_title: Optional[str] = Field(...,description="대회 이름",example="BDMNTN XL")
    nation_code: str = Field(...,description="국가 코드 (예: KR, US, JP 등)",example="KR")
    city_name: Optional[str] = Field(
        None,
        description="도시 이름",
        example="서울"
    )
    stadium_name: Optional[str] = Field(
        None,
        description="경기장 이름",
        example="장충체육관"
    )
    is_bxl: Optional[bool] = Field(
        None,
        description="BXL 여부 (Y/N 등)",
        example="Y"
    )
    start_date: Optional[str] = Field(
        None,
        description="대회 시작 날짜 (yyyy-mm-dd 형식)",
        example="2025-01-01"
    )
    end_date: Optional[str] = Field(
        None,
        description="대회 종료 날짜 (yyyy-mm-dd 형식)",
        example="2025-01-10"
    )

class PlayerInfo(BaseModel):
    """
    개별 플레이어 정보를 나타내는 모델
    """
    player_uuid: Optional[uuid.UUID] = Field(
        default=None,
        description="플레이어 UUID. 기존 플레이어가 아닌 경우 None."
    )
    first_name: str = Field(
        ...,
        description="플레이어의 퍼스트(이름) 부분",
        example="Eko"
    )
    family_name: str = Field(
        ...,
        description="플레이어의 패밀리(성) 부분",
        example="Yuli"
    )
    nick_name: str = Field(
        ...,
        description="플레이어의 별칭(닉네임)",
        example="Eko Y."
    )
    nation_code: str = Field(
        ...,
        description="플레이어 국적(2~4 글자 코드, 예: KOR, USA, etc.)",
        example="KOR"
    )
    gender: str = Field(
        ...,
        description="플레이어 성별(M=남, W=여 등)",
        example="M"
    )
    hand: str = Field(
        ...,
        description="플레이어가 주로 사용하는 손('right' 또는 'left')",
        example="right"
    )
    primary_discipline: str = Field(
        ...,
        description="플레이어의 주종목(SGL=단식, DBL=복식, MXD=혼합복식)",
        example="SGL"
    )

class TeamAndPlayerInfo(BaseModel):
    """
    팀과 플레이어 정보를 한 번에 받기 위한 Pydantic 모델
    - 'team_code'가 없으면 새 팀을 생성할 수도 있고,
    - 이미 존재하는 'team_code'가 있다면 해당 팀에 플레이어를 등록 또는 업데이트
    """
    tournament_uuid: uuid.UUID = Field(...,description="해당 팀과 플레이어가 속한 대회(Tournament)의 고유 식별자(UUID).",
                                       example="d290f1ee-6c54-4b01-90e6-d701748f0851")
    team_name: str = Field(...,description="팀 이름. 동일한 국적(nation_code) 내에서는 중복될 수 없습니다.",example="Warriors")
    team_code: Optional[int] = Field(None, description="team_info 테이블의 PK(고유번호). 값을 주지 않으면 새로 팀이 생성될 수 있습니다.", example=1)
    players_info: List[PlayerInfo] = Field( ...,description="하나의 플레이어 정보를 나타내는 중첩 객체" )

class MatchInfo(BaseModel):
    """각 매치 정보"""
    match_no: int = Field(..., description="매치 번호 (1~5)")
    match_type: str = Field(..., description="매치 유형 (예: MSIG, WSIG, MDBL, WDBL, 03X3)")
    match_point: int = Field(..., description="매치 포인트(단식=1, 복식=2, 3대3=3)")
    team1_player: List[uuid.UUID] = Field(...,description="TEAM1 선수 UUID 배열")
    team2_player: List[uuid.UUID] = Field(...,description="TEAM2 선수 UUID 배열")

class TieInfo(BaseModel):
    """전체 전달받는 경기 정보 구조"""
    tournament_uuid: uuid.UUID = Field(...,description="토너먼트(대회) UUID (예: '96189024-2c80-4937-92e9-c80936a7baf9')")
    tie_no: int = Field(...,description="Tie 번호 (예: 1)")
    game_date: str = Field(...,description="경기 일자 (YYYY-MM-DD 형식)")
    team1_code: int = Field(...,description="팀1 코드 (예: 1)")
    team2_code: int = Field(...,description="팀2 코드 (예: 2)")
    match_info: List[MatchInfo] = Field(...,description="매치 정보 리스트 (최대 5경기)")

class OfficialInfo(BaseModel):
    """
    운영 요원(Official) 정보 구조

    - `official_uuid`: 운영 요원의 고유 UUID (API 내부에서 자동으로 생성됨)
    - `first_name`: 운영 요원의 이름 (예: 길동)
    - `family_name`: 운영 요원의 성 (예: 홍)
    - `nickname`: 운영 요원의 별칭
    - `gender`: 운영 요원의 성별 (예: M, F, Other 등)
    """
    official_uuid: uuid.UUID = Field( default=None, description="운영 요원의 고유 UUID (API에서 자동 생성되며, 별도 입력 불필요)" )
    first_name: str = Field( ..., description="운영 요원의 이름 (예: 길동)" )
    family_name: str = Field( ..., description="운영 요원의 성 (예: 홍)" )
    nickname: str = Field(..., description="운영 요원의 별칭 (필요 시 작성)" )
    gender: str = Field( ..., description="운영 요원의 성별 (예: M, F, Other 등)" )
    nation_code: str = Field(...,description="운영 요원의 3자리 국가 코드 (예: KOR, USA 등)")

class OfficialSearch(BaseModel):
    """
    운영 요원(Official) 정보 구조

    - `official_uuid`: 운영 요원의 고유 UUID (API 내부에서 자동으로 생성됨)
    - `first_name`: 운영 요원의 이름 (예: 길동)
    - `family_name`: 운영 요원의 성 (예: 홍)
    - `nickname`: 운영 요원의 별칭
    - `gender`: 운영 요원의 성별 (예: M, F, Other 등)
    """
    official_uuid: uuid.UUID = Field( default=None, description="운영 요원의 고유 UUID (API에서 자동 생성되며, 별도 입력 불필요)" )
    first_name: str = Field( None, description="운영 요원의 이름 (예: 길동)" )
    family_name: str = Field( None, description="운영 요원의 성 (예: 홍)" )
    nickname: str = Field(None, description="운영 요원의 별칭 (필요 시 작성)" )
    gender: str = Field( None, description="운영 요원의 성별 (예: M, F, Other 등)" )
    nation_code: str = Field(None,description="운영 요원의 3자리 국가 코드 (예: KOR, USA 등)")


class GameOfficialInfo(BaseModel):
    """
    게임에 할당되는 운영 요원(Officials)에 대한 정보 모델

    - `game_uuid`: 경기 식별자 (bxl.game_info.game_uuid)
    - `official_uuid`: 운영 요원 식별자 (bxl.official_info.official_uuid)
    - `official_role`: 운영 요원 역할 (예: 'UMPIRE', 'SERVICE_JUDGE', 'LINE_JUDGE', 'REFEREE', 'SCORER' 등)
    """

    game_uuid: uuid.UUID = Field(..., description="경기 식별자 (bxl.game_info.game_uuid)" )
    official_uuid: uuid.UUID = Field(..., description="운영 요원 식별자 (bxl.official_info.official_uuid)" )
    official_role: str = Field(..., description="운영 요원 역할 (예: UMPIRE, SERVICE_JUDGE, LINE_JUDGE, REFEREE, SCORER 등)" )

