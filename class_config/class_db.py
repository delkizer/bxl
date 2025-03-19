# -*- coding: utf-8 -*-
"""
Created on 2024-12-01

@author: island78
"""
from dataclasses import dataclass, field
from typing import Optional

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from class_config.class_env import Config


@dataclass
class ConfigDB:
    config = Config()

    bxl: Optional[sqlalchemy.engine.base.Engine] = field(default=None, init=False)

    bxl_session_factory: Optional[sessionmaker] = field(default=None, init=False)

    def _initialize_engine(self, db_url: str):
        # SQLAlchemy Core 엔진 초기화
        return create_engine(
            db_url,
            pool_size=20,           # 풀 크기 설정 (예: 20)
            max_overflow=10,        # 최대 초과 연결 수 (풀링이 초과되었을 때)
            pool_timeout=30,        # 풀에서 연결을 가져올 때 최대 대기 시간 (초)
            pool_recycle=1800       # 연결이 재활용되기 전까지 유지되는 시간 (초)
        )

    def _initialize_session_factory(self, engine):
        # SQLAlchemy Core에서 세션 팩토리를 초기화
        return sessionmaker(bind=engine)

    def get_bxl_session_factory(self, config):
        if not self.bxl:
            try:
                # 필수 설정 값 확인
                required_attrs = ["postgres_user", "postgres_pass", "postgres_host", "postgres_port",
                                  "postgres_db_name_spotv"]
                for attr in required_attrs:
                    if not hasattr(config, attr):
                        raise AttributeError(f"⚠️ Config에 {attr} 속성이 없습니다.")

                # DB 연결 URL 생성
                bxl_url = f"postgresql+psycopg2://{config.postgres_user}:{config.postgres_pass}" \
                          f"@{config.postgres_host}:{config.postgres_port}/{config.postgres_db_name_spotv}" \
                          f"?client_encoding=utf8"
                #print(f"Connecting to {bxl_url}")

                # 데이터베이스 엔진 및 세션 팩토리 초기화
                self.bxl = self._initialize_engine(bxl_url)
                self.bxl_session_factory = self._initialize_session_factory(self.bxl)

                if not self.bxl_session_factory:
                    raise RuntimeError("❌ bxl_session_factory 초기화 실패!")

            except AttributeError as e:
                print(f"🔴 AttributeError 발생: {e}")
                raise

            except Exception as e:
                print(f"🔴 DB 연결 오류 발생: {e}")
                raise

        return self.bxl_session_factory

    def close_connections(self):
        try:
            if self.bxl:
                self.bxl.dispose()
                self.bxl = None

        except Exception as e:
            print(f"Error while closing database connections: {e}")
