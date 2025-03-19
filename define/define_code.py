from typing import Final

class DefineCode:
    TASK_STATUS_INIT: Final[str] = 'I'  #initialized
    TASK_STATUS_RUN: Final[str] = 'R'   #running
    TASK_STATUS_ERR: Final[str] = 'E'   #error

    MONIT_URI: Final[str] = '/monit/kbo-operation'
    MONIT_TYPE_TASK_UPDATE: Final[str] = 'task_update'
    MONIT_STATUS_INIT: Final[str] = 'INIT'
    MONIT_STATUS_RUN: Final[str] = 'RUN'
    MONIT_STATUS_ERR: Final[str] = 'ERR'
    MONIT_STATUS_CRASH: Final[str] = 'CRASH'

    JWT_ALGORITHM:Final[str] = "RS256"
