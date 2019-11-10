import os
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .cmds import BtoIrCmd, CameraCmd
from .config import MODEL_FILE, INPUT_SIZE
from .database import SessionLocal, engine
from .predictor import Predictor


models.Base.metadata.create_all(bind=engine)
app = FastAPI(bto_ir_cmd=BtoIrCmd(),
              camera_cmd=CameraCmd(),
              predictor=Predictor(MODEL_FILE, INPUT_SIZE))


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.post("/codes/{key}", response_model=schemas.Code)
def create_code(key: str, db: Session = Depends(get_db)):
    db_code = crud.get_code_by_key(db, key=key)
    if db_code:
        raise HTTPException(status_code=400,
                            detail="Code already registered")
    code = schemas.CodeCreate(
        key=key,
        code=app.extra['bto_ir_cmd'].receive()
    )
    return crud.create_code(db=db, code=code)


@app.get("/codes/", response_model=List[schemas.Code])
def read_codes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    codes = crud.get_codes(db, skip=skip, limit=limit)
    return codes


@app.post('/codes/{key}/transmit', response_model=schemas.TransmitResponse)
def transmit_code(key: str, db: Session = Depends(get_db)):
    db_code = crud.get_code_by_key(db, key=key)
    if db_code is None:
        raise HTTPException(status_code=404, detail="Code not found")
    app.extra['bto_ir_cmd'].transmit(db_code.code)
    file_path = app.extra['camera_cmd'].run()
    label, _ = app.extra['predictor'].predict(file_path)
    return {'on': bool(label)}


@app.delete('/codes/{key}', response_model=schemas.Code)
def delete_code(key: str, db: Session = Depends(get_db)):
    db_code = crud.get_code_by_key(db, key=key)
    if db_code is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return crud.delete_code(db=db, key=key)
