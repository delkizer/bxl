import uuid
from datetime import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from fastapi import HTTPException, status

from class_config.class_db import ConfigDB
from class_config.class_env import Config
from class_lib.api.base_model import TieInfo
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

    def create_tie(self, tie_info: TieInfo):
        session = self.bxl_session_factory()
        try:
            game_date_obj = None
            if tie_info.game_date:
                game_date_obj = datetime.strptime(tie_info.game_date, "%Y-%m-%d").date()

            game_uuid = None

            # insert 쿼리 (Postgres)
            insert_sql = text("""
                              INSERT INTO bxl.game_info (game_uuid, tournament_uuid, tie_no, match_no, game_no, match_type, match_point
                                  ,team1_code, team2_code, game_date, created_at, updated_at, match_status, game_status)
                              VALUES (:game_uuid, :tournament_uuid, :tie_no, :match_no, :game_no, :match_type, :match_point
                                  ,:team1_code, :team2_code, :game_date,now(), now(), 'SCHEDULED', 'SCHEDULED')
                              """)

            # match_info 배열에 대해 반복 INSERT/UPDATE
            for match in tie_info.match_info:
                #모든 게임은 5경기 발생한다
                params = {}
                for game_no in range(1, 6):
                    game_uuid = uuid.uuid4()
                    # 바운드 파라미터 구성
                    params = {
                        "game_uuid": game_uuid,
                        "tournament_uuid": tie_info.tournament_uuid,
                        "tie_no": tie_info.tie_no,
                        "match_no": match.match_no,
                        "game_no": game_no,
                        "match_type": match.match_type,
                        "match_point": match.match_point,
                        "team1_code": tie_info.team1_code,
                        "team2_code": tie_info.team2_code,
                        "game_date": game_date_obj,
                    }

                    result = session.execute(insert_sql, params)
                    # INSERT/UPDATE 후 RETURNING game_uuid
                    self.logger.info(f"Insert match_no={match.match_no}, game_no={game_no} => game_uuid={game_uuid}")

                    #각 매치의 player 숫자 만큼 INSERT
                    upsert_player_sql = text("""
                            INSERT INTO bxl.game_player_info( game_uuid, player_uuid, team_code, created_at, updated_at )
                            VALUES ( :game_uuid, :player_uuid, :team_code, now(), now() )
                            """)

                    # 1) 팀1 선수들
                    for p_uuid in match.team1_player:
                        session.execute( upsert_player_sql, {
                                "game_uuid": game_uuid,
                                "player_uuid": p_uuid,
                                "team_code": tie_info.team1_code
                            }
                        )

                    # 2) 팀2 선수들
                    for p_uuid in match.team2_player:
                        session.execute( upsert_player_sql, {
                                "game_uuid": game_uuid,
                                "player_uuid": p_uuid,
                                "team_code": tie_info.team2_code
                            }
                        )

            session.commit()
            return {"msg": "Game info insert completed successfully"}
        except IntegrityError as e:
            session.rollback()
            self.logger.error(f"Game info creation failed (IntegrityError): {e}")
            # 여기서 필요한 에러 처리(예: 중복 에러 메시지)
            raise HTTPException(status_code=400, detail="중복 제약 위반 혹은 무결성 오류가 발생하였습니다.")

        except Exception as e:
            session.rollback()
            self.logger.error(f"Game info creation failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")


    def get_tie_list(self, tournament_uuid, tie_no):
        session = self.bxl_session_factory
        try:
            base_sql = """
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
            if tie_no:
                where_clauses.append("tie_no = :tie_no")
                params["tie_no"] = tie_no

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
