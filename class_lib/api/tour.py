from datetime import datetime

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
            MERGE INTO bxl.tournament_info AS t
            USING (
              VALUES (
                  :tournament_uuid, :tournament_title, :nation_code, :city_name, :stadium_name, :is_bxl
                  , :start_date, :end_date )
            ) AS v (
                uuid, title, n_code, c_name, s_name, bxl_flag, s_date, e_date )
            ON t.tournament_uuid = v.uuid   -- PK(또는 UNIQUE) 컬럼 기준 매칭
            WHEN MATCHED THEN
            UPDATE
            SET tournament_title = v.title,
                nation_code      = v.n_code,
                city_name        = v.c_name,
                stadium_name     = v.s_name,
                is_bxl           = v.bxl_flag,
                start_date       = v.s_date,
                end_date         = v.e_date
            WHEN NOT MATCHED THEN
            INSERT (
                tournament_uuid, tournament_title, nation_code, city_name, stadium_name, is_bxl
                , start_date, end_date )
            VALUES (
                uuid_generate_v4(), v.title, v.n_code, v.c_name, v.s_name, v.bxl_flag, v.s_date, v.e_date )
             """)

            start_date_obj = datetime.strptime(tourinfo.start_date, '%Y-%m-%d').date()
            end_date_obj = datetime.strptime(tourinfo.end_date, '%Y-%m-%d').date()

            session.execute(query,             {
                "tournament_uuid": tourinfo.tournament_uuid,
                "tournament_title": tourinfo.tournament_title,
                "nation_code": tourinfo.nation_code,
                "city_name": tourinfo.city_name,
                "stadium_name": tourinfo.stadium_name,
                "is_bxl": tourinfo.is_bxl,
                "start_date": start_date_obj,
                "end_date": end_date_obj
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

    def tour_list(self, tournament_uuid):
        session = self.bxl_session_factory()
        try:
            base_query = """
                SELECT A.tournament_uuid, A.tournament_title, A.city_name, A.start_date, A.end_date
                     , A.nation_code, A.stadium_name, B.code_desc as nation_name 
                FROM bxl.tournament_info A
                INNER JOIN bxl.code_info B ON A.nation_code = B.code
                WHERE is_bxl = true
                {WHERE}
             """

            # 조건을 담을 리스트
            where_clauses = []
            # 바인딩할 파라미터
            params = {}

            # tournament_uuid 조건
            if tournament_uuid:
                where_clauses.append("AND tournament_uuid = :tournament_uuid")
                params["tournament_uuid"] = tournament_uuid

            final_where = ""
            if where_clauses:
                final_where = " AND ".join(where_clauses)

            # base_sql의 {WHERE}를 final_where로 교체
            final_sql = base_query.replace("{WHERE}", final_where)
            query = text(final_sql)
            result = session.execute(query, params).mappings().all()

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
