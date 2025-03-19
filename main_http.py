import traceback
import requests
import json

from fastapi import FastAPI, Path, Query, HTTPException, Depends, status, Body
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, Dict

from class_config.class_env import Config
from class_config.class_log import ConfigLogger
from class_config.class_db import ConfigDB
from class_config.class_define import Define

from class_lib.api.auth import Auth
from define.define_code import DefineCode
from custom_exception import BaseProjectError, PrivateKeyNotFoundError


# 기본 클래스 설정
config = Config()
config_logger = ConfigLogger('http_log', 365)
logger = config_logger.get_logger('fastapi')
define = Define()
define_code = DefineCode()
db_config = ConfigDB()

auth = Auth( logger, db_config.get_astm_admin_session_factory() )

# title, description 등 OpenAPI 문서용 설정을 줄 수 있음
app = FastAPI(
    title="trackman-kbo-operation",
    description="kbo-operation 관련 API를 모두 통합",
    version="0.0.1",
    docs_url="/api/docs",               # Swagger UI 라우트
    redoc_url="/api/redoc",             # Redoc 라우트 (원하면 삭제 가능)
    openapi_url="/api/openapi.json",    # OpenAPI JSON
)

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

@app.get("/api/hello/{name}", tags=["Sample"])
async def say_hello(
        name: str = Path(..., description="사용자 이름 (경로 파라미터)")
):
    """
    - path parameter `name`을 받아서 "Hello {name}"을 반환
    """
    return {"message": f"Hello {name}"}

@app.post("/api/sessions_info", tags=["CMS"],
          summary="{data}에 도착한 날자에 인입된 session feed 정보를 제공",
          response_model=Dict[str, GetSessionInfo],
          responses={
             200: {"description": "조회 결과 성공 ",
                   "content": {
                       "application/json": {
                           "example": {
                                        "ca6d3547-4376-4a48-94bb-b5cc1c3da3d9": {
                                            "HomeTeam_Name": "Jeju HS",
                                            "AwayTeam_Name": "JoongAng High School",
                                            "GameReference": "20240519-Mokdong-1",
                                            "Field_Name": "Mokdong Baseball Stadium",
                                            "Field_ShortName": "Mokdong",
                                            "League_ShortName": "Team",
                                            "SessionStartedLocal": "2024-11-20T04:03:21.9290913+00:00"
                                        },
                                        "55c000f2-5fcf-4063-a860-a0728f25a661": {
                                            "HomeTeam_Name": "kt wiz",
                                            "AwayTeam_Name": "",
                                            "GameReference": "20240519-Suwon-BP-1",
                                            "Field_Name": "Suwon Baseball Stadium",
                                            "Field_ShortName": "Suwon",
                                            "League_ShortName": None,
                                            "SessionStartedLocal": "2024-11-20T04:03:21.9290913+00:00"
                                        }
                           }
                    }
                }
            },
             401: {"description": "만료된 토큰 등 인증 실패"},
             500: {"description": "서버 내부 에러"}
         })

async def get_sessions_info(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        query: SessionQuery = Body(...)
):
    """
    - v3.sessions 테이블에 존재하는 피드 조회
    - start_date ~ end_date 범위의 SessionId를 key로, GetSessionInfo 구조를 value로 하는 Dict를 반환
    """
    try:
        auth.get_jwt_verify(credentials)
    except HTTPException as e:
        logger.error(e)
        raise e

    try:
        sessions_list = cms.get_session_info(query.start_date, query.end_date)
        result_dict = {}
        for session_item in sessions_list:
            packet_str = session_item.get("packet")
            if not packet_str:
                # packet 키 자체가 없거나 빈 문자열인 경우
                continue

            try:
                packet_list = json.loads(packet_str)
                # packet_list가 빈 리스트일 수도 있으므로 대비
                if not packet_list:
                    continue
                packet = packet_list[0]
            except (json.JSONDecodeError, IndexError):
                # JSON 파싱 실패 혹은 리스트 인덱스 실패
                continue
            data = packet.get("data", {})

            home_team = data.get("HomeTeam", {})
            away_team = data.get("AwayTeam", {})
            league = data.get("League", {})
            location = data.get("Location", {})
            field = location.get("Field", {})
            session_id = data.get("SessionId")
            sessionstate = data.get("SessionState")

            result_info = {
                "HomeTeam_Name": home_team.get("Name", None),
                "AwayTeam_Name": away_team.get("Name", None),
                "GameReference": data.get("GameReference", None),
                "Field_Name": field.get("Name", None),
                "Field_ShortName": field.get("ShortName", None),
                "League_ShortName": league.get("ShortName", None),
                "SessionStartedLocal": sessionstate.get("SessionStartedLocal", None),
            }

            result_dict[session_id] = result_info
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    except HTTPException as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return result_dict

@app.get("/api/token/verify", tags=["AUTH"],
         summary="발급한 jwt 토큰 검증",
         responses={
             200: {"description": "JWT 토큰 인증 성공"},
             401: {"description": "만료된 토큰 등 인증 실패"},
             403: {"description": "서명 불일치(변조) 등 권한 없음"},
             422: {"description": "검증 불가 (잘못된 포맷, 요청 파라미터 에러 등)"}
         })
async def token_verify(
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
):
    """
    - Bearer 토큰을 헤더로 받고, RS256으로 디코딩
    - DB 조회
    - 유효하면 200 응답
    - 만료, 무효, 기타 에러 시 적절한 4xx or 5xx
    """
    try:
        auth.get_jwt_verify(credentials)
        return {"detail": "JWT 인증 성공"}
    except HTTPException as err:
        logger.error(err)
        traceback.print_exc()
        raise err

@app.get("/api/token/jwt_refresh", tags=["AUTH"],
         summary="발급한 jwt 토큰 검증 후 만료되었을 때 토큰 검증 후 재발행",
         responses={
             200: {"description": "JWT 토큰 인증 성공"},
             401: {"description": "만료된 토큰 등 인증 실패"},
             403: {"description": "서명 불일치(변조) 등 권한 없음"},
             422: {"description": "검증 불가 (잘못된 포맷, 요청 파라미터 에러 등)"}
         })
async def token_jwt_refresh(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))
):
    """
    - 토큰 리프레시를 예로 든 엔드포인트
    - verify_jwt_token_or_raise() 사용
    - Timeout 발생 시 구글 인증 로직 등 추가 처리
    """
    logger.info(f"credentials: {credentials}")
    try:
        auth.get_jwt_verify(credentials)
        return {"detail": "JWT 토큰 갱신 성공"}

    except HTTPException as http_ex:
        # 1) 401이 아닌 경우 인 경우는 "서버 내부 에러"로 그대로 재전달
        if http_ex.status_code != status.HTTP_401_UNAUTHORIZED:
            raise http_ex

        try:
            logger.error(f"[token_refresh] 401 error => Google 인증 유도: {http_ex.detail}")
            token_info = auth.get_google_verify(credentials)
            if token_info:
                email = token_info["email"]
                sub = token_info["providers"]
                new_jwt = auth.get_jwt_token(email, sub, 1)  # 예시
                auth.insert_cms_admins_01( email, sub, token_info, new_jwt)

                return {"detail": "JWT refreshed", "token": new_jwt}
        except BaseProjectError as e:
            logger.error(f"[token_refresh] {e}", traceback.format_exc())
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="JWT refreshed") from e

    except BaseProjectError as e:
        logger.error(f"[token_refresh] Unknown exception => 500: {e}", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@app.get("/api/auth/login/google/", tags=["AUTH"],
         summary="Google OAuth 로그인 요청",
         responses={
             302: {"description": "구글 OAuth 로그인 페이지로 리다이렉트"},
             400: {"description": "요청이 잘못되었을 때 (hostname 인식 등)"}
         })
def google_login():
    """
    구글 OAuth2 인증을 시작하기 위한 엔드포인트.

    1) 환경(Hostname)에 따라 redirect_uri를 결정
    2) 구글 인증 페이지 URL을 구성
    3) RedirectResponse를 통해 사용자를 구글로 넘김
    """
    redirect_uri = auth.get_redirect_uri()
    if not redirect_uri:
        raise HTTPException(status_code=400, detail="Failed to determine redirect_uri")

    # 구글 OAuth 인증 페이지 URL 구성
    # 필요에 따라 scope, access_type, prompt 등 매개변수 수정 가능
    google_auth_url = (
        f"{config.google_auth_uri}"
        f"?client_id={config.google_client_id}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope={config.google_scope}"
        f"&access_type=offline"
        f"&prompt=consent"
        f"&state=state_parameter_passthrough_value"
    )

    print(f"google_auth_url: {google_auth_url}")
    logger.info(f"[google_login] Redirecting to Google auth URL: {google_auth_url}")

    # 302 Redirect
    return RedirectResponse(url=google_auth_url)

@app.get("/api/auth/complete/google/", tags=["AUTH"],
         summary="Google OAuth callback",
         response_model=TokenExchangeResponse,
         responses={
             302: {"description": "리다이렉트 성공: 프론트엔드로 JWT 전달 후 이동"},
             400: {"model": TokenExchangeError},
             500: {"description": "구글 토큰 교환 실패 등 내부 서버 오류"},
         })
def google_callback(
        code: str = Query(None, description="Authorization code from Google"),
        error: str = Query(None, description="Error param from Google callback")
):
    """
    구글 인증 후 리다이렉트되는 콜백 엔드포인트.

    - **code**: 구글 OAuth Authorization Code
    - **error**: 구글에서 전달된 에러 문자열 (있다면 400 에러 반환)

    **성공 시**:
    - 302 Redirect: 프론트엔드(/login/done)로 이동, 쿼리 파라미터에 JWT 첨부

    **실패 시**:
    - 400: error 파라미터 존재, 또는 code가 None
    - 500: 구글 토큰 교환 실패
    """
    if error:
        raise HTTPException(status_code=400, detail=f"Google returned error: {error}")

    if not code:
        raise HTTPException(status_code=400, detail="No code in callback")

    # 구글에 토큰 교환 요청
    redirect_uri = auth.get_redirect_uri()
    if not redirect_uri:
        raise HTTPException(status_code=400, detail="Failed to determine redirect_uri")

    front_uri = auth.get_front_uri()
    if not front_uri:
        raise HTTPException(status_code=400, detail="Failed to determine front_uri")

    token_url = "https://oauth2.googleapis.com/token"
    params = {
        "code": code,
        "client_id": config.google_client_id,
        "client_secret": config.google_client_secret,
        "redirect_uri": redirect_uri,
        "grant_type": "authorization_code"
    }
    logger.info(f"google token exchange params: {params}")
    response = requests.post(token_url, data=params)
    if response.status_code == 200:
        try:
            email = None
            token_data = response.json()

            access_token = token_data.get("access_token", "")
            resp = requests.get(
                "https://www.googleapis.com/oauth2/v3/userinfo",
                headers={"Authorization": f"Bearer {access_token}"}
            )
            if resp.status_code == 200:
                user_info = resp.json()
                email = user_info.get("email")
            else:
                logger.error(f"google user_info get Error {resp.text}", traceback.format_exc())
                raise HTTPException(status_code=500, detail="google user_info(Email) get Error")
            #logger.info(f"google token exchange response: {token_data}")

            custom_jwt = auth.get_jwt_token(email=email, sub=define_code.TOKEN_PROVIDER_GOOGLE, expires_hours=1)
            try:
                auth.insert_cms_admins_01(email, define_code.TOKEN_PROVIDER_GOOGLE, token_data, custom_jwt)

            except BaseProjectError as e:
                logger.error(f"astm_admin DB set Error {e}", traceback.format_exc())
                raise HTTPException(status_code=e.status_code, detail=e.message)

            return RedirectResponse(f"{front_uri}/auth/login/done?jwt={custom_jwt}")

        except PrivateKeyNotFoundError as e:
            logger.error(f"Token exchange failed: {e.status_code} {e.message}", traceback.format_exc())
            raise HTTPException(status_code=e.status_code, detail=e.message)

        except BaseProjectError as e:
            raise HTTPException(status_code=e.status_code, detail=e.message)
    else:
        logger.error(f"Token exchange failed: {response.text}")
        raise HTTPException(status_code=500, detail="Token exchange failed")

