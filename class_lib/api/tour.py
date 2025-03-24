from fastapi import HTTPException
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError
from starlette import status

from class_config.class_db import ConfigDB
from class_config.class_env import Config
from class_lib.local_utils.utils import Utils
from class_lib.api.base_model import TourInfo
from define.define_code import DefineCode


class Tour:
    def __init__(self, logger):
        self.config = Config()
        self.class_name = __name__.split(".")[-1].replace('class_', '')
        self.logger = logger
        self.define_code = DefineCode()
        self.utils = Utils(self.logger)
        self.db = ConfigDB()
        self.bxl_session_factory = self.db.get_bxl_session_factory(self.config)

    def create_tour(self, tourinfo: TourInfo):
        session = self.bxl_session_factory()
        try:
            query = text("""
                INSERT INTO bxl.tournament_info (
                    tournament_uuid, tournament_title, nation_code, city_name, stadium_name
                    , is_bxl, start_date, end_date
                ) 
                VALUES (
                    uuid_generate_v4(), :tournament_title, :nation_code, :city_name, :stadium_name
                    , :is_bxl, :start_date, :end_date
                )
             """)
            session.execute(query,             {
                "tournament_title": tourinfo.tournament_title,
                "nation_code": tourinfo.nation_code,
                "city_name": tourinfo.city_name,
                "stadium_name": tourinfo.stadium_name,
                "is_bxl": tourinfo.is_bxl,
                "start_date": tourinfo.start_date,
                "end_date": tourinfo.end_date
            })
            session.commit()
            return {"msg": "Tournament created successfully"}

        except IntegrityError as e:
            session.rollback()

            error_msg = str(e.orig).lower()  # or str(e).lower()

            if "unique_tournament_title" in error_msg:
                raise HTTPException(status_code=409, detail="이미 동일한 대회명이 존재합니다.")
            elif "unique_nation_city_dates" in error_msg:
                raise HTTPException(status_code=409, detail="해당 국가, 도시, 기간으로 이미 등록된 대회가 있습니다.")
            else:
                raise HTTPException(status_code=400, detail="중복 제약 위반이 발생하였습니다.")

        except Exception as e:
            session.rollback()
            self.logger.error(f"User creation failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            session.close()

    def nation_list(self):
        session = self.bxl_session_factory()
        try:
            query = text("""
                SELECT code, code_desc
                FROM bxl.code_info
                WHERE code_group = 'nation_code' ORDER BY code
             """)
            result = session.execute(query).mappings().all()

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            return result

        except HTTPException as http_exc:
            # HTTPException을 그대로 재전달
            raise http_exc

        except Exception as e:
            session.rollback()
            self.logger.error(f"User creation failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            session.close()
