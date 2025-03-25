import uuid

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
        self.bxl_sesstion_factory = self.db.get_bxl_session_factory(self.config)

    def create_team_and_player(self, team_player_info: TeamAndPlayerInfo):
        session = self.bxl_sesstion_factory()
        try:
            if team_player_info.team_code is None:
                # 새 팀 INSERT
                new_team_code = self._insert_team(session, team_player_info)
            else:
                # 기존 팀 UPDATE
                new_team_code = self._update_team(session, team_player_info)

            for player in team_player_info.players_info:
                if player.player_uuid is None:
                    # player_uuid가 없으면 새로 INSERT
                    new_player_uuid = self._insert_player(
                        session=session,
                        team_code=new_team_code,
                        tournament_uuid=team_player_info.tournament_uuid,
                        player=player
                    )
                    # 필요하다면 new_player_uuid를 player.player_uuid에 할당
                    player.player_uuid = new_player_uuid
                else:
                    # player_uuid가 있으면 UPDATE
                    updated_count = self._update_player(
                        session=session,
                        team_code=new_team_code,
                        tournament_uuid=team_player_info.tournament_uuid,
                        player=player
                    )
                    # 혹은 업데이트된 행이 없는 경우 에러 처리 등도 가능:
                    if updated_count == 0:
                        raise HTTPException(status_code=404, detail=f"Player not found: {player.player_uuid}")

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

    def _insert_team(self, session, team_player_info: TeamAndPlayerInfo) -> int:
        insert_sql = text("""
                          INSERT INTO bxl.team_info (tournament_uuid, team_name, nation_code)
                          VALUES (:tournament_uuid, :team_name, :nation_code) RETURNING team_code
                          """)
        result = session.execute(insert_sql, {
            "tournament_uuid": str(team_player_info.tournament_uuid),
            "team_name": team_player_info.team_name,
            "nation_code": team_player_info.nation_code
        })
        return result.scalar()  # 새로 생성된 PK

    def _update_team(self, session, team_player_info: TeamAndPlayerInfo) -> int:
        update_sql = text("""
                          UPDATE bxl.team_info
                          SET tournament_uuid = :tournament_uuid,
                              team_name       = :team_name,
                              nation_code     = :nation_code
                          WHERE team_code = :team_code
                          """)
        session.execute(update_sql, {
            "team_code": team_player_info.team_code,
            "tournament_uuid": str(team_player_info.tournament_uuid),
            "team_name": team_player_info.team_name,
            "nation_code": team_player_info.nation_code
        })
        return team_player_info.team_code

    def _insert_player(self, session, team_code: int, tournament_uuid: uuid.UUID, player: PlayerInfo) -> uuid.UUID:
        """
        새 플레이어를 INSERT하고, 생성된 UUID를 반환.
        player_uuid가 None이면 여기서 새로 생성해서 INSERT.
        """
        # 1) player_uuid가 없으면 새로 생성
        new_uuid = uuid.uuid4()

        insert_sql = text("""
                          INSERT INTO bxl.player_info
                              (player_uuid, team_code, tournament_uuid, player_name, gender)
                          VALUES (:player_uuid, :team_code, :tournament_uuid, :player_name,
                                  :gender) RETURNING player_uuid
                          """)

        result = session.execute(insert_sql, {
            "player_uuid": str(new_uuid),
            "team_code": team_code,
            "tournament_uuid": str(tournament_uuid),
            "player_name": player.player_name,
            "gender": player.gender
        })
        return result.scalar()  # 새로 삽입된 UUID

    def _update_player(self, session, team_code: int, tournament_uuid: uuid.UUID, player: PlayerInfo) -> int:
        """
        기존 플레이어를 UPDATE.
        리턴값: 업데이트된 행 수(rowcount)

        - 존재하지 않는 player_uuid에 대해 UPDATE를 시도하면 rowcount=0
        - 여기서 처리할지, 상위에서 처리할지 결정 가능
        """
        update_sql = text("""
                          UPDATE bxl.player_info
                          SET team_code       = :team_code,
                              tournament_uuid = :tournament_uuid,
                              player_name     = :player_name,
                              gender          = :gender
                          WHERE player_uuid = :player_uuid
                          """)
        result = session.execute(update_sql, {
            "player_uuid": str(player.player_uuid),
            "team_code": team_code,
            "tournament_uuid": str(tournament_uuid),
            "player_name": player.player_name,
            "gender": player.gender
        })
        return result.rowcount
