from typing import List

from pydantic import BaseModel


class CodeBase(BaseModel):
    code_key: str
    code_str: str = None


class CodeCreate(CodeBase):
    pass


class Code(CodeBase):
    code_id: int

    class Config:
        orm_mode = True
