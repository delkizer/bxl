import uuid
from typing import Optional, List
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
    tournament_uuid: uuid.UUID = Field(
        ...,
        description="해당 팀과 플레이어가 속한 대회(Tournament)의 고유 식별자(UUID).",
        example="d290f1ee-6c54-4b01-90e6-d701748f0851"
    )
    team_name: str = Field(
        ...,
        description="팀 이름. 동일한 국적(nation_code) 내에서는 중복될 수 없습니다.",
        example="Warriors"
    )
    team_code: Optional[int] = Field(
        None,
        description="team_info 테이블의 PK(고유번호). 값을 주지 않으면 새로 팀이 생성될 수 있습니다.",
        example=1
    )
    players_info: List[PlayerInfo] = Field(
        ...,
        description="하나의 플레이어 정보를 나타내는 중첩 객체"
    )

