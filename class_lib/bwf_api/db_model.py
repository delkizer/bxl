import uuid
from sqlalchemy import Column, String, CHAR
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class OfficialInfoModel(Base):
    """
    운영 요원(Official) 정보 구조 (bxl.official_info)
    """
    __tablename__ = 'official_info'
    __table_args__ = {'schema': 'bxl'}

    official_uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        comment="운영 요원의 고유 UUID (API에서 자동 생성되며, 별도 입력 불필요)"
    )
    first_name = Column(
        String(100),
        nullable=False,
        comment="운영 요원의 이름 (예: 길동)"
    )
    family_name = Column(
        String(100),
        nullable=False,
        comment="운영 요원의 성 (예: 홍)"
    )
    nickname = Column(
        String(100),
        nullable=False,
        comment="운영 요원의 별칭 (필요 시 작성)"
    )
    gender = Column(
        String(20),
        nullable=False,
        comment="운영 요원의 성별 (예: M, F, Other 등)"
    )
    nation_code = Column(
        CHAR(3),
        nullable=False,
        comment="운영 요원의 3자리 국가 코드 (예: KOR, USA 등)"
    )
