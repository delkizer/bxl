import uuid
from typing import List, Optional

from fastapi import HTTPException, status, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text

from class_lib.api.base_model import OfficialInfo, GameOfficialInfo, OfficialSearch
from class_config.class_db import ConfigDB
from class_config.class_env import Config
from class_lib.api.db_model import OfficialInfoModel
from class_lib.local_utils import utils
from define.define_code import DefineCode


class Officials:
    def __init__(self, logger):
        self.config = Config()
        self.class_name = __name__.split(".")[-1].replace('class_', '')
        self.logger = logger
        self.define_code = DefineCode()
        self.utils = utils.Utils(self.logger)
        self.db = ConfigDB()
        self.bxl_session_factory = self.db.get_bxl_session_factory(self.config)

    def official_info_query(
            self,
            official_uuid: Optional[uuid.UUID] = Query(None),
            first_name: Optional[str] = Query(None),
            family_name: Optional[str] = Query(None),
            nickname: Optional[str] = Query(None),
            gender: Optional[str] = Query(None),
            nation_code: Optional[str] = Query(None)
    ) -> OfficialInfo:
        return OfficialInfo(
            official_uuid=official_uuid,
            first_name=first_name,
            family_name=family_name,
            nickname=nickname,
            gender=gender,
            nation_code=nation_code
        )

    def get_officials(self
                      , official_info: OfficialSearch
                      ):
        session = self.bxl_session_factory()
        try:
            query = session.query(OfficialInfoModel)
            if official_info is not None:
                if official_info.official_uuid is not None:
                    query = query.filter(OfficialInfoModel.official_uuid == official_info.official_uuid)
                if official_info.first_name:
                    query = query.filter(OfficialInfoModel.first_name == official_info.first_name)
                if official_info.family_name:
                    query = query.filter(OfficialInfoModel.family_name == official_info.family_name)
                if official_info.nickname:
                    query = query.filter(OfficialInfoModel.nickname.ilike(f"{official_info.nickname}%"))
                if official_info.gender:
                    query = query.filter(OfficialInfoModel.gender == official_info.gender)
                if official_info.nation_code:
                    query = query.filter(OfficialInfoModel.nation_code == official_info.nation_code)

            result = query.all()

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



    def get_gameties(self, tournament_uuid):
        session = self.bxl_session_factory()
        try:
            query = text("""
                SELECT A.tie_no, A.match_no
                FROM bxl.game_info A
                WHERE A.tournament_uuid = :tournament_uuid
                GROUP BY A.tie_no, A.match_no
                ORDER BY A.tie_no ASC, A.match_no ASC
             """)
            result = session.execute(query, {
                'tournament_uuid': tournament_uuid,
            }).mappings().all()

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            tie_dict = {}

            for row in result:
                tie_no = row['tie_no']
                match_no = row['match_no']

                # tie_no가 처음 나오면 초기화
                if tie_no not in tie_dict:
                    tie_dict[tie_no] = []
                # match_no 추가
                tie_dict[tie_no].append(match_no)

            tie_info_list = []
            for tie_no, match_list in tie_dict.items():
                # match_list를 정렬하고 싶다면 sorted() 사용
                tie_info_list.append({
                    "tie_no": tie_no,
                    "match_no": match_list
                })

            result_json = {
                "tournament_uuid": tournament_uuid,
                "tie_info": tie_info_list
            }

            return result_json

        except HTTPException as http_exc:
            # HTTPException을 그대로 재전달
            raise http_exc

        except Exception as e:
            session.rollback()
            self.logger.error(f"User creation failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            session.close()

    def get_gameuuids(self, tournament_uuid, tie_no, match_no):
        session = self.bxl_session_factory()
        try:
            query = text("""
                SELECT A.game_no, A.game_uuid
                FROM bxl.game_info A
                WHERE A.tournament_uuid = :tournament_uuid
                AND A.tie_no = :tie_no AND A.match_no = :match_no
                ORDER BY A.match_no ASC, A.game_no
             """)
            result = session.execute(query, {
                'tournament_uuid': tournament_uuid,
                'tie_no': tie_no,
                'match_no': match_no,
            }).mappings().all()

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            result_json = {
                "tournament_uuid": tournament_uuid,
                "tie_no": tie_no,
                "match_no": match_no,
                "game_uuids" : result
            }
            return result_json

        except HTTPException as http_exc:
            # HTTPException을 그대로 재전달
            raise http_exc

        except Exception as e:
            session.rollback()
            self.logger.error(f"User creation failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            session.close()


    def post_officials(self, officials:List[OfficialInfo]):
        session = self.bxl_session_factory()
        try:
            insert_query = text("""
                INSERT INTO bxl.official_info 
                    (official_uuid, first_name, family_name, nickname, gender, nation_code)
                VALUES 
                    (:official_uuid, :first_name, :family_name, :nickname, :gender, :nation_code)
            """)

            for official_data in officials:
                # official_uuid가 없으면 Python 측에서 생성
                new_uuid = official_data.official_uuid or uuid.uuid4()

                params = {
                    "official_uuid": str(new_uuid),      # uuid 객체 → str 변환
                    "first_name": official_data.first_name,
                    "family_name": official_data.family_name,
                    "nickname": official_data.nickname,
                    "gender": official_data.gender,
                    "nation_code": official_data.nation_code,
                }

                session.execute(insert_query, params)


            session.commit()
            return {"msg": "Officials created successfully"}

        except IntegrityError as e:
            session.rollback()
            error_msg = str(e.orig).lower()  # or str(e).lower()
            self.logger.error(f"Official creation failed: {e}^{error_msg}")
            raise HTTPException(status_code=500, detail="Internal server error")

        except Exception as e:
            session.rollback()
            self.logger.error(f"Official creation failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

        finally:
            session.close()

    def put_officials(self, officials: List[OfficialInfo]):
        """
        여러 Official 정보를 한꺼번에 수정하는 예시 (Full Update)
        - official_uuid 기준으로 레코드 식별
        - 존재하지 않으면 어떻게 처리할지(신규 생성 vs 에러) 정책 결정 필요
        """
        session = self.bxl_session_factory()
        try:
            # 1) UPDATE 쿼리 텍스트 준비
            update_query = text("""
                UPDATE bxl.official_info
                   SET first_name   = :first_name,
                       family_name  = :family_name,
                       nickname     = :nickname,
                       gender       = :gender,
                       nation_code  = :nation_code
                 WHERE official_uuid = :official_uuid
            """)

            for official_data in officials:
                # 여기서는 official_uuid가 필수. 없으면 업데이트할 레코드 식별 불가능
                if not official_data.official_uuid:
                    raise HTTPException(status_code=400, detail="official_uuid is required for update.")

                params = {
                    "official_uuid": str(official_data.official_uuid),
                    "first_name": official_data.first_name,
                    "family_name": official_data.family_name,
                    "nickname": official_data.nickname,
                    "gender": official_data.gender,
                    "nation_code": official_data.nation_code,
                }

                session.execute(update_query, params)

            session.commit()
            return {"msg": "Officials updated successfully"}

        except IntegrityError as e:
            session.rollback()
            error_msg = str(e.orig).lower()
            self.logger.error(f"Official update failed: {e}^{error_msg}")
            raise HTTPException(status_code=500, detail="Internal server error")

        except Exception as e:
            session.rollback()
            self.logger.error(f"Official update failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

        finally:
            session.close()

    def delete_officials(self, officials: List[OfficialInfo]):
        """
        여러 Official 정보를 한꺼번에 삭제 (official_uuid만 있으면 충분)
        """

        session = self.bxl_session_factory()
        try:
            # DELETE 쿼리 준비
            delete_query = text("""
                DELETE FROM bxl.official_info
                 WHERE official_uuid = :official_uuid
            """)

            for official_data in officials:
                if not official_data.official_uuid:
                    raise HTTPException(
                        status_code=400,
                        detail="official_uuid is required for deletion."
                    )

                params = {"official_uuid": str(official_data.official_uuid)}
                session.execute(delete_query, params)

            session.commit()
            return {"msg": "Officials deleted successfully"}

        except IntegrityError as e:
            session.rollback()
            error_msg = str(e.orig).lower()
            self.logger.error(f"Official delete failed: {e}^{error_msg}")
            raise HTTPException(status_code=500, detail="Internal server error")

        except Exception as e:
            session.rollback()
            self.logger.error(f"Official delete failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

        finally:
            session.close()

    def post_gameofficial(self, game_official_list: List[GameOfficialInfo]):
        session = self.bxl_session_factory()
        try:
            # INSERT 쿼리 준비
            insert_query = text("""
                                INSERT INTO bxl.game_official_info
                                    (game_uuid, official_uuid, official_role)
                                VALUES (:game_uuid, :official_uuid, :official_role)
                                """)

            # 여러 GameOfficialInfo 객체를 순회하면서 삽입
            for official_data in game_official_list:
                params = {
                    "game_uuid": str(official_data.game_uuid),
                    "official_uuid": str(official_data.official_uuid),
                    "official_role": official_data.official_role,
                }
                session.execute(insert_query, params)

            session.commit()
            return {"msg": "GameOfficials created successfully"}

        except IntegrityError as e:
            session.rollback()
            error_msg = str(e.orig).lower()
            self.logger.error(f"GameOfficial creation failed: {e}^{error_msg}")
            # 실제 제약 이름에 따라 조건 처리 (예: 중복 PK 등)
            raise HTTPException(status_code=400, detail="중복 제약 위반 또는 무결성 오류 발생")

        except Exception as e:
            session.rollback()
            self.logger.error(f"GameOfficial creation failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

        finally:
            session.close()

    def put_gameofficials(self, game_official_list: List[GameOfficialInfo]):
        session = self.bxl_session_factory()
        try:
            # UPDATE 쿼리 준비
            update_query = text("""
                                UPDATE bxl.game_official_info
                                SET official_role = :official_role
                                WHERE game_uuid = :game_uuid
                                  AND official_uuid = :official_uuid
                                """)

            for official_data in game_official_list:
                # 필수 식별자 체크
                if not official_data.game_uuid or not official_data.official_uuid:
                    raise HTTPException(status_code=400, detail="game_uuid and official_uuid are required for update.")

                params = {
                    "game_uuid": str(official_data.game_uuid),
                    "official_uuid": str(official_data.official_uuid),
                    "official_role": official_data.official_role,
                }
                session.execute(update_query, params)

            session.commit()
            return {"msg": "GameOfficials updated successfully"}

        except IntegrityError as e:
            session.rollback()
            error_msg = str(e.orig).lower()
            self.logger.error(f"GameOfficial update failed: {e}^{error_msg}")
            # 실제 제약 이름, 무결성 에러를 확인 후 적절히 처리
            raise HTTPException(status_code=400, detail="무결성 제약 또는 중복 키 에러")

        except Exception as e:
            session.rollback()
            self.logger.error(f"GameOfficial update failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

        finally:
            session.close()

    def delete_gameofficials(self, game_official_list: List[GameOfficialInfo]):
        session = self.bxl_session_factory()
        try:
            delete_query = text("""
                                DELETE
                                FROM bxl.game_official_info
                                WHERE game_uuid = :game_uuid
                                  AND official_uuid = :official_uuid
                                """)

            for official_data in game_official_list:
                if not official_data.game_uuid or not official_data.official_uuid:
                    raise HTTPException(status_code=400,
                                        detail="game_uuid and official_uuid are required for deletion.")

                params = {
                    "game_uuid": str(official_data.game_uuid),
                    "official_uuid": str(official_data.official_uuid),
                }
                session.execute(delete_query, params)

            session.commit()
            return {"msg": "GameOfficials deleted successfully"}

        except IntegrityError as e:
            session.rollback()
            error_msg = str(e.orig).lower()
            self.logger.error(f"GameOfficial delete failed: {e}^{error_msg}")
            raise HTTPException(status_code=500, detail="무결성 제약 또는 DB 오류")

        except Exception as e:
            session.rollback()
            self.logger.error(f"GameOfficial delete failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

        finally:
            session.close()