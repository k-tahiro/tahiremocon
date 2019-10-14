from sqlalchemy import Column, Integer, String

from .database import Base


class Code(Base):
    __tablename__ = "codes"

    code_id = Column(Integer, primary_key=True, index=True)
    code_key = Column(String, unique=True, index=True)
    code_str = Column(String)
