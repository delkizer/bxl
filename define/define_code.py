from typing import Final

class DefineCode:
    GAME_STATUS_PRE_GAME: Final[str] = "Pre_Game"
    GAME_STATUS_ON_PROGRESS: Final[str] = "On-Progress"
    GAME_STATUS_ON_FINAL: Final[str] = "Final"

    CHANNEL_CODE_NBA:Final[str] = 'nba'
    CHANNEL_CODE_KOVO:Final[str]  = 'kovo'
    CHANNEL_CODE_KBL:Final[str]  = 'kbl'
    CHANNEL_CODE_BETMAN:Final[str]  = 'betman'
    CHANNEL_CODE_SPOTVBET:Final[str]  = 'spotvbet'
    CHANNEL_CODE_KBO_HOMERUN:Final[str]  = 'kbo_homerun'
    CHANNEL_CODE_KBO_CATCHER:Final[str] = 'catcher'
    CHANNEL_CODE_MLB:Final[str]  = 'mlb'
    CHANNEL_CODE_SOCC:Final[str]  = 'socc'
    CHANNEL_CODE_TRACKMAN_CHECK:Final[str]  = 'trackman_check'
    CHANNEL_CODE_PLAYER_INFO_CHANGE:Final[str]  = 'player_info_change'
    CHANNEL_CODE_KBO_OPERATION:Final[str]  = 'kbo_operation'

    GAME_TYPE_RS: Final[str] = 'R'    # 정규 시즌 (Regular Season)
    GAME_TYPE_EX: Final[str] = 'S'    # 시범 경기 (Exhibition)
    GAME_TYPE_WC: Final[str] = 'W'    # 와일드 카드 (Wild Card)
    GAME_TYPE_PO: Final[str] = 'PT'   # 플레이 오프 (Play-Off)
    GAME_TYPE_KS: Final[str] = 'K'    # 한국 시리즈 (Korean Series)
    GAME_TYPE_RD: Final[str] = 'RD'   # 순위 결정전 (Ranking Decider)
    GAME_TYPE_MP: Final[str] = 'M'    # 준 플레이 오프 (Minor Play-Off)

    TASK_STATUS_INIT: Final[str] = 'I'  #initialized
    TASK_STATUS_RUN: Final[str] = 'R'   #running
    TASK_STATUS_ERR: Final[str] = 'E'   #error

    MONIT_URI: Final[str] = '/monit/kbo-operation'
    MONIT_TYPE_TASK_UPDATE: Final[str] = 'task_update'
    MONIT_STATUS_INIT: Final[str] = 'INIT'
    MONIT_STATUS_RUN: Final[str] = 'RUN'
    MONIT_STATUS_ERR: Final[str] = 'ERR'
    MONIT_STATUS_CRASH: Final[str] = 'CRASH'

    LEAGUE_KBO:Final[str] = 'KBO1'

    JWT_ALGORITHM:Final[str] = "RS256"
    TOKEN_PROVIDER_GOOGLE:Final[str] = 'GOOGLE'
