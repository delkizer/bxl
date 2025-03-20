from typing import Optional
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
