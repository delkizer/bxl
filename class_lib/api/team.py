import uuid

from starlette import status
from fastapi import HTTPException
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError

from class_config.class_db import ConfigDB
from class_config.class_env import Config
from class_lib.api.base_model import TeamAndPlayerInfo, PlayerInfo
from class_lib.local_utils.utils import Utils
from define.define_code import DefineCode


class Team:
    def __init__(self, logger):
        self.config = Config()
        self.class_name = __name__.split(".")[-1].replace('class_', '')
        self.logger = logger
        self.define_code = DefineCode()
        self.utils = Utils(self.logger)
        self.db = ConfigDB()
        self.bxl_session_factory = self.db.get_bxl_session_factory(self.config)

    def get_player_list(self, team_code: str):
        session = self.bxl_session_factory()
        try:
            query = text("""
                SELECT A.team_code, A.team_name, A.tournament_uuid
                , B.player_uuid
                , B.first_name, B.family_name, B.nick_name, B.hand, B.primary_discipline
                , trim(B.nation_code) as nation_code, trim(B.gender) as gender
                FROM bxl.team_info A
                LEFT OUTER JOIN bxl.player_info B ON A.team_code = B.team_code
                WHERE A.team_code = :team_code
                ORDER BY gender ASC, B.nick_name ASC 
            """)
            result = session.execute(query, {
                "team_code": team_code
            }).mappings().all()

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Team not found",
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

    def get_team_list(self):
        session = self.bxl_session_factory()
        try:
            query = text("""
                SELECT A.tournament_title, A.tournament_uuid
                , A.city_name, A.start_date, A.end_date
                , B.team_code, B.team_name
                , ( SELECT count(*) FROM bxl.player_info pi WHERE pi.team_code = B.team_code) as player_cnt
                FROM bxl.tournament_info A
                INNER JOIN bxl.team_info B ON A.tournament_uuid = B.tournament_uuid
                WHERE A.is_bxl = true
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


    def create_team_and_player(self, team_player_info: TeamAndPlayerInfo):
        session = self.bxl_session_factory()
        try:
            if team_player_info.team_code is None:
                # 새 팀 INSERT
                new_team_code = self._insert_team(session, team_player_info)
            else:
                # 기존 팀 UPDATE
                new_team_code = self._update_team(session, team_player_info)

            existing_players = self._team_player_list(
                session,
                team_player_info.team_code if team_player_info.team_code else new_team_code
            )
            # RowMapping -> dict 형태의 map { player_uuid: RowMapping }
            existing_players_map = {
                p["player_uuid"]: p for p in existing_players if p["player_uuid"]
            }

            incoming_uuids = {p.player_uuid for p in team_player_info.players_info if p.player_uuid}

            #DB에는 있으나 새 요청에 없는 uuid들 → 삭제
            for old_uuid, old_player_obj in existing_players_map.items():
                if old_uuid not in incoming_uuids:
                    # (1) game_player_info 삭제
                    self._delete_game_player(session, new_team_code, old_uuid)

                    # (2) player_info 삭제
                    self._delete_player(session, new_team_code, old_uuid)

                    # (3) 히스토리 테이블 기록 (DELETE)
                    deleted_player_info = PlayerInfo(
                        player_uuid=old_uuid,
                        first_name=old_player_obj["first_name"],
                        family_name=old_player_obj["family_name"],
                        nick_name=old_player_obj["nick_name"],
                        nation_code=old_player_obj["nation_code"],
                        gender=old_player_obj["gender"],
                        hand=old_player_obj["hand"],
                        primary_discipline=old_player_obj["primary_discipline"]
                    )

                    self._insert_player_history(
                        session=session,
                        dml_type="DELETE",
                        team_code=new_team_code,
                        tournament_uuid=old_player_obj["tournament_uuid"],
                        player=deleted_player_info
                    )

            for player_info in team_player_info.players_info:
                if not player_info.player_uuid:
                    # a) player_uuid 없는 신규 -> INSERT
                    new_player_uuid = self._insert_player(
                        session=session,
                        team_code=new_team_code,
                        tournament_uuid=team_player_info.tournament_uuid,
                        player=player_info
                    )
                    player_info.player_uuid = new_player_uuid

                    # 히스토리 기록
                    self._insert_player_history(
                        session=session,
                        dml_type="INSERT",
                        team_code=new_team_code,
                        tournament_uuid=team_player_info.tournament_uuid,
                        player=player_info
                    )
                else:
                    # b) player_uuid가 있고 DB에도 존재하면 -> UPDATE
                    if player_info.player_uuid in existing_players_map:
                        self._update_player(
                            session=session,
                            team_code=new_team_code,
                            tournament_uuid=team_player_info.tournament_uuid,
                            player=player_info
                        )

                        # 히스토리 기록 (UPDATE)
                        self._insert_player_history(
                            session=session,
                            dml_type="UPDATE",
                            team_code=new_team_code,
                            tournament_uuid=team_player_info.tournament_uuid,
                            player=player_info
                        )
                    else:
                        # c) player_uuid는 있으나 DB에 없는 경우 -> INSERT
                        new_player_uuid = self._insert_player(
                            session=session,
                            team_code=new_team_code,
                            tournament_uuid=team_player_info.tournament_uuid,
                            player=player_info
                        )
                        player_info.player_uuid = new_player_uuid

                        # 히스토리 기록 (INSERT)
                        self._insert_player_history(
                            session=session,
                            dml_type="INSERT",
                            team_code=new_team_code,
                            tournament_uuid=team_player_info.tournament_uuid,
                            player=player_info
                        )

            session.commit()
            return {"msg": "team and player created successfully"}

        except IntegrityError as e:
            self.logger.error(f"User creation failed: {e}")
            session.rollback()
            error_msg = str(e.orig).lower()  # or str(e).lower()
            if "team_info_nation_code_team_name_uq" in error_msg:
                raise HTTPException(status_code=409, detail="이미 동일한 팀명이 존재합니다.")
            elif "player_info_team_tournament_name_gender_uq" in error_msg:
                raise HTTPException(status_code=409, detail="이미 동일한 이름이 존재합니다.")
            else:
                raise HTTPException(status_code=400, detail="중복 제약 위반이 발생하였습니다.")

        except Exception as e:
            session.rollback()
            self.logger.error(f"User creation failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            session.close()

    def _team_player_list(self, session, team_code):
        query = text("""
            SELECT player_uuid, tournament_uuid, first_name, family_name, nick_name
                 , nation_code, gender, hand, primary_discipline
            FROM bxl.player_info
            WHERE team_code = :team_code
         """)
        result = session.execute(query, {"team_code": team_code}).mappings().all()
        return result

    def _insert_team(self, session, team_player_info: TeamAndPlayerInfo) -> int:
        insert_sql = text("""
                          INSERT INTO bxl.team_info (tournament_uuid, team_name)
                          VALUES (:tournament_uuid, :team_name) RETURNING team_code
                          """)
        result = session.execute(insert_sql, {
            "tournament_uuid": str(team_player_info.tournament_uuid),
            "team_name": team_player_info.team_name,
        })
        return result.scalar()  # 새로 생성된 PK

    def _update_team(self, session, team_player_info: TeamAndPlayerInfo) -> int:
        update_sql = text("""
                          UPDATE bxl.team_info
                          SET tournament_uuid = :tournament_uuid,
                              team_name       = :team_name
                          WHERE team_code = :team_code
                          """)
        session.execute(update_sql, {
            "team_code": team_player_info.team_code,
            "tournament_uuid": str(team_player_info.tournament_uuid),
            "team_name": team_player_info.team_name,
        })
        return team_player_info.team_code

    def _insert_player(self, session, team_code: int, tournament_uuid: uuid.UUID, player: PlayerInfo) -> uuid.UUID:
        """
        새 플레이어를 INSERT하고, 생성된 UUID를 반환.
        player_uuid가 None이면 여기서 새로 생성해서 INSERT.
        """
        # 1) player_uuid가 None이면 새로 생성
        new_uuid = player.player_uuid or uuid.uuid4()

        insert_sql = text("""
                          INSERT INTO bxl.player_info (player_uuid, team_code, tournament_uuid, first_name, family_name
                              , nick_name, nation_code, gender, hand, primary_discipline)
                          VALUES (:player_uuid, :team_code, :tournament_uuid, :first_name, :family_name
                                , :nick_name, :nation_code, :gender, :hand, :primary_discipline) RETURNING player_uuid
                          """)

        result = session.execute(insert_sql, {
            "player_uuid": str(new_uuid),
            "team_code": team_code,
            "tournament_uuid": str(tournament_uuid),
            "first_name": player.first_name,
            "family_name": player.family_name,
            "nick_name": player.nick_name,
            "nation_code": player.nation_code,
            "gender": player.gender,
            "hand": player.hand,
            "primary_discipline": player.primary_discipline,
        })
        return result.scalar()

    def _update_player(self, session, team_code: int, tournament_uuid: uuid.UUID, player: PlayerInfo) -> int:
        """
        기존 플레이어를 UPDATE한다.
        리턴값: 업데이트된 행 수(rowcount)
        """
        update_sql = text("""
                          UPDATE bxl.player_info
                          SET team_code          = :team_code,
                              tournament_uuid    = :tournament_uuid,
                              first_name         = :first_name,
                              family_name        = :family_name,
                              nick_name          = :nick_name,
                              nation_code        = :nation_code,
                              gender             = :gender,
                              hand               = :hand,
                              primary_discipline = :primary_discipline
                          WHERE player_uuid = :player_uuid
                          """)

        result = session.execute(update_sql, {
            "player_uuid": str(player.player_uuid),
            "team_code": team_code,
            "tournament_uuid": str(tournament_uuid),

            "first_name": player.first_name,
            "family_name": player.family_name,
            "nick_name": player.nick_name,
            "nation_code": player.nation_code,
            "gender": player.gender,
            "hand": player.hand,
            "primary_discipline": player.primary_discipline
        })
        return result.rowcount

    def _delete_player(self, session, team_code: int, player_uuid: uuid.UUID):
        delete_sql = text("""
                DELETE FROM bxl.player_info WHERE team_code = :team_code AND player_uuid = :player_uuid
                """)
        result = session.execute(delete_sql, {"team_code": team_code, "player_uuid": player_uuid})
        return result

    def _delete_game_player(self, session, team_code: int, player_uuid: uuid.UUID):
        delete_sql = text("""
                DELETE FROM bxl.game_player_info WHERE team_code = :team_code AND player_uuid = :player_uuid
                """)
        result = session.execute(delete_sql, {"team_code": team_code, "player_uuid": player_uuid})
        return result

    def _insert_player_history( self, session, dml_type: str, team_code: int
                                , tournament_uuid: uuid.UUID, player: PlayerInfo ):
        insert_sql = text("""
                          INSERT INTO bxl.player_history
                            (dml_type, player_uuid, team_code, tournament_uuid, first_name, family_name
                            , nick_name, nation_code, gender, hand, primary_discipline, create_time)
                          VALUES 
                            (:dml_type, :player_uuid, :team_code, :tournament_uuid, :first_name, :family_name
                            , :nick_name, :nation_code, :gender, :hand, :primary_discipline, now())
                          """)

        result = session.execute(insert_sql, {
            "dml_type": dml_type,
            "player_uuid": player.player_uuid,
            "team_code": team_code,
            "tournament_uuid": tournament_uuid,
            "first_name": player.first_name,
            "family_name": player.family_name,
            "nick_name": player.nick_name,
            "nation_code": player.nation_code,
            "gender": player.gender,
            "hand": player.hand,
            "primary_discipline": player.primary_discipline,
        })
        return result
