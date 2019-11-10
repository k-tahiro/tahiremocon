from sqlalchemy.orm import Session

from . import models, schemas
from .cmds import BtoIrCmd


def get_code(db: Session, id_: int):
    return db.query(models.Code).filter(models.Code.id == id_).first()


def get_code_by_key(db: Session, key: str):
    return db.query(models.Code).filter(models.Code.key == key).first()


def get_codes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Code).offset(skip).limit(limit).all()


def create_code(db: Session, code: schemas.CodeCreate):
    db_code = models.Code(**code.dict())
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code


def delete_code(db: Session, key: str):
    db_code = get_code_by_key(db, key)
    db.delete(db_code)
    db.commit()
    return db_code
