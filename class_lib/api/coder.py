import uuid

from sqlalchemy.sql import text
from fastapi import HTTPException, status

from class_config.class_db import ConfigDB
from class_config.class_env import Config
from class_lib.local_utils import utils
from define.define_code import DefineCode


class Coder:
    def __init__(self, logger):
        self.config = Config()
        self.class_name = __name__.split(".")[-1].replace('class_', '')
        self.logger = logger
        self.define_code = DefineCode()
        self.utils = utils.Utils(self.logger)
        self.db = ConfigDB()
        self.bxl_session_factory = self.db.get_bxl_session_factory(self.config)

    def get_game_list(self, game_date: str, tournament_uuid: uuid.UUID):
        query = None
        session = self.bxl_session_factory()
        try:
            base_sql = """
                SELECT A.*
                , B.team_name as team1_name
                , C.team_name as team2_name
                , DENSE_RANK() OVER (ORDER BY A.game_date) AS day_num
                FROM ( 
                        SELECT tie_no, team1_code, team2_code, game_date
                        , SUM(CASE WHEN winner_team_code = team1_code THEN match_point ELSE 0 END) AS team1_point_sum
                        , SUM(CASE WHEN winner_team_code = team2_code THEN match_point ELSE 0 END) AS team2_point_sum
                        FROM bxl.game_info
                        {WHERE}
                        GROUP BY tie_no, team1_code, team2_code, game_date ) A
                INNER JOIN bxl.team_info B ON A.team1_code = B.team_code
                INNER JOIN bxl.team_info C ON A.team2_code = C.team_code
            """

            # 조건을 담을 리스트
            where_clauses = []
            # 바인딩할 파라미터
            params = {}

            # tournament_uuid 조건
            if tournament_uuid:
                where_clauses.append("tournament_uuid = :tournament_uuid")
                params["tournament_uuid"] = tournament_uuid

            # game_date 조건
            if game_date:
                where_clauses.append("game_date = :game_date")
                params["game_date"] = game_date

            # 최종 WHERE 문자열 만들기
            final_where = ""
            if where_clauses:
                final_where = "WHERE " + " AND ".join(where_clauses)

            # base_sql의 {WHERE}를 final_where로 교체
            final_sql = base_sql.replace("{WHERE}", final_where)

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
            self.logger.error(f"Error authenticate_user querying the database for query^{query}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
                headers={"WWW-Authenticate": "Bearer"},
            )
        finally:
            session.close()
