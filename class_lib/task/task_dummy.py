import sys
import time
import threading
import asyncio

from typing import Final
from datetime import datetime

from class_config.class_env import Config
from class_config.class_log import ConfigLogger
from class_config.class_db import ConfigDB

class TaskDummy:
    TASK_NAME: Final[str] = __name__.split('.')[-1].replace('class_', '')  # 현재 파일의 이름에서 자동으로 태스크 이름 설정
    DESCRIPTION: Final[str] = ("This is a dummy task designed for testing and development purposes. "
                               "It performs no business logic but instead simulates a task by running "
                               "for a fixed amount of time (5 seconds).")

    def __init__(self):
        self.config = Config()
        self.class_name = __name__.split('.')[-1].replace('class_', '')
        config_logger = ConfigLogger(self.class_name , 365)
        self.logger = config_logger.get_logger('fastapi')
        self.db = None
        self.mlb_session_factory = None
        self.last_update_timestamp = None  # 비즈니스 로직의 마지막 실행 타임스탬프
        self.task_name = "dummy"

    def initialize_db_connection(self):
        # 프로세스 내부에서 DB 연결을 새로 생성하는 메서드
        self.db = ConfigDB()
        self.mlb_session_factory = self.db.get_mlb_session_factory( self.config )
        self.logger.info(f"Database connection initialized for {self.class_name}..")

    """빈 작업 클래스: 비즈니스 로직 없이 기본적으로 작동하는 형태만을 구현"""
    async def run(self):
        # 메인 동기 작업
        self.logger.info(f"{self.task_name} is running...")
        self.initialize_db_connection()

        # 예외 발생 시 crash 상태 전송
        try:
            self._start_thread()
        except Exception as e:
            self.logger.error(f"Critical error occurred: {e}")
            sys.exit(1)

        # 비즈니스 로직 스레드가 종료될 때까지 기다림
        while self.business_logic_thread.is_alive():
            await asyncio.sleep(1)

    def _start_thread(self):
        # 비즈니스 로직 스레드
        self.logger.info("Starting business logic thread...")
        self.business_logic_thread = threading.Thread(target=self.business_logic_wrapper, daemon=True)
        self.business_logic_thread.start()

    def business_logic_wrapper(self):
        try:
            # 비즈니스 로직 실행
            self._run_business_logic_task()
        except Exception as e:
            # 비즈니스 로직 실행 중 예외가 발생하면 로깅 및 상태 업데이트
            self.logger.error(f"Exception in business logic thread: {e}")

    def _run_business_logic_task(self):
        """비즈니스 로직을 수행"""
        attempt = 0
        while True:
            try:
                # 더미 비즈니스 로직: 5초 대기 후 상태 업데이트
                time.sleep(5)
                self.last_update_timestamp = datetime.now().isoformat()  # 현재 시간을 ISO 포맷으로 저장
                self.logger.info(f"Last update timestamp: {self.last_update_timestamp}")
                '''
                #치명적인 오류 발생
                if attempt == 3:
                    raise RuntimeError("Critical error occurred! Simulating a fatal business logic error.")
                else:
                    attempt += 1                
                '''

            except Exception as e:
                # 비즈니스 로직에 문제가 발생한 경우 상태를 'error'로 변경
                self.logger.error(f"[Error in business logic: {e}")
                raise


