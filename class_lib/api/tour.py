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

    def delete_tour(self, tournament_uuid):
        session = self.bxl_session_factory()
        try:
            delete_query = text("""
                DELETE FROM bxl.tournament_info
                WHERE tournament_uuid = :tournament_uuid
            """)
            result = session.execute(delete_query, {"tournament_uuid": tournament_uuid})

            # 삭제된 행이 없으면 해당 대회가 존재하지 않음을 의미
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Tournament not found")

            session.commit()
            return {"msg": "Tournament deleted successfully"}

        except Exception as e:
            session.rollback()
            self.logger.error(f"Tournament deletion failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

        finally:
            session.close()

    def create_tour(self, tourinfo: TourInfo):
        session = self.bxl_session_factory()
        try:
            # 문자열 날짜를 date 객체로 변환 (None일 경우 처리)
            start_date_obj = datetime.strptime(tourinfo.start_date, '%Y-%m-%d').date() if tourinfo.start_date else None
            end_date_obj = datetime.strptime(tourinfo.end_date, '%Y-%m-%d').date() if tourinfo.end_date else None

            if tourinfo.tournament_uuid:
                # tournament_uuid가 제공된 경우 UPDATE 실행
                self._update_tournament(session, tourinfo, start_date_obj, end_date_obj)
                msg = "Tournament updated successfully"
            else:
                # tournament_uuid가 없으면 새 레코드 INSERT
                self._insert_tournament(session, tourinfo, start_date_obj, end_date_obj)
                msg = "Tournament created successfully"

            session.commit()
            return {"msg": msg}

        except IntegrityError as e:
            session.rollback()
            error_msg = str(e.orig).lower()
            if "unique_tournament_title" in error_msg:
                raise HTTPException(status_code=409, detail="이미 동일한 대회명이 존재합니다.")
            elif "unique_nation_city_dates" in error_msg:
                raise HTTPException(status_code=409, detail="해당 국가, 도시, 기간으로 이미 등록된 대회가 있습니다.")
            else:
                raise HTTPException(status_code=400, detail="중복 제약 위반이 발생하였습니다.")

        except Exception as e:
            session.rollback()
            self.logger.error(f"Tournament creation/update failed: {e}")
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

    def get_matchtype_list(self):
        session = self.bxl_session_factory()
        try:
            query = text("""
            SELECT code, code_desc AS match_type
              FROM bxl.code_info
             WHERE code_group = 'match_type'
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

    def _insert_tournament(self, session, tourinfo: TourInfo, start_date_obj, end_date_obj):
        insert_query = text("""
            INSERT INTO bxl.tournament_info (
                tournament_uuid, tournament_title, nation_code, city_name, stadium_name,
                is_bxl, start_date, end_date
            )
            VALUES (
                uuid_generate_v4(), :tournament_title, :nation_code, :city_name, :stadium_name,
                :is_bxl, :start_date, :end_date
            )
        """)
        session.execute(insert_query, {
            "tournament_title": tourinfo.tournament_title,
            "nation_code": tourinfo.nation_code,
            "city_name": tourinfo.city_name,
            "stadium_name": tourinfo.stadium_name,
            "is_bxl": tourinfo.is_bxl,
            "start_date": start_date_obj,
            "end_date": end_date_obj
        })

    def _update_tournament(self, session, tourinfo: TourInfo, start_date_obj, end_date_obj):
        update_query = text("""
            UPDATE bxl.tournament_info
               SET tournament_title = :tournament_title,
                   nation_code      = :nation_code,
                   city_name        = :city_name,
                   stadium_name     = :stadium_name,
                   is_bxl           = :is_bxl,
                   start_date       = :start_date,
                   end_date         = :end_date
             WHERE tournament_uuid = :tournament_uuid
        """)
        session.execute(update_query, {
            "tournament_uuid": tourinfo.tournament_uuid,
            "tournament_title": tourinfo.tournament_title,
            "nation_code": tourinfo.nation_code,
            "city_name": tourinfo.city_name,
            "stadium_name": tourinfo.stadium_name,
            "is_bxl": tourinfo.is_bxl,
            "start_date": start_date_obj,
            "end_date": end_date_obj
        })