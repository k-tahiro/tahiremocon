from pydantic import BaseModel


class CodeBase(BaseModel):
    key: str
    code: str = None


class CodeCreate(CodeBase):
    pass


class Code(CodeBase):
    id: int

    class Config:
        orm_mode = True


class TransmitResponse(BaseModel):
    success: bool
    label: int = -1
