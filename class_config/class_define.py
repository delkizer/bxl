from typing import Final

class Define:
    #process의 상태값
    PROC_STATUS_STOP: Final[str] = "0"
    PROC_STATUS_START: Final[str] = "1"
    PROC_STATUS_RUN : Final[str] = "2"
    PROC_STATUS_TERMINATED: Final[str] = "3"
    PROC_STATUS_UNKNOWN : Final[str] = "9"

    #process의 종류
    PROC_TYPE_SOCKET: Final[str] = "socket"
    PROC_TYPE_SQS: Final[str] = "sqs_client"

    #내부 API 정보
    API_URL: Final[str] = "http://127.0.0.1:8300"
    API_NAME_MONITOR_TIMESTAMP_INSERT: Final[str] = "insert"
    API_NAME_MONITOR_TIMESTAMP_UPDATE: Final[str] = "update"
    API_NAME_MONITOR_TIMESTAMP_TERMINATE: Final[str] = "terminate"

    API_NAME_MONITOR_OPERATE_RETRIEVE: Final[str] = "retrieve"
    API_NAME_MONITOR_OPERATE_RESTART: Final[str] = "restart"

    API_NAME_SERVICE_RESTART: Final[str] = "restart"

    #API ERROR CODE
    ERROR_CODE_SUCCESS:Final[str] = "0000"
    ERROR_CODE_WARN: Final[str] = "0001"
    ERROR_CODE_JSON_ERROR:Final[str] = "0100"
    ERROR_CODE_DB_ERROR:Final[str] = "0501"
    ERROR_CODE_PROC_LOOKUP_ERROR:Final[str] = "2701"
    ERROR_CODE_CALLED_PROC_ERROR:Final[str] = "2702"
    ERROR_CODE_ETC:Final[str] = "9999"

    #websockat 정보
    WEBSOCKET_URL: Final[str] = "ws://127.0.0.1:8301/ws"