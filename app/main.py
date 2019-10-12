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


@app.post('/codes/receive')
def receive_code():
    return app.extra['bto_ir_cmd'].receive()


@app.post("/codes/", response_model=schemas.Code)
def create_code(code: schemas.CodeCreate, db: Session = Depends(get_db)):
    db_code = crud.get_code_by_key(db, key=code.code_key)
    if db_code:
        raise HTTPException(status_code=400,
                            detail="Code already registered")
    if code.code_str is None:
        code.code_str = receive_code()
    return crud.create_code(db=db, code=code)


@app.get("/codes/", response_model=List[schemas.Code])
def read_codes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    codes = crud.get_codes(db, skip=skip, limit=limit)
    return codes


@app.post('/codes/{code_key}')
def transmit_code(code_key: str, db: Session = Depends(get_db)):
    db_code = crud.get_code_by_key(db, key=code_key)
    if db_code is None:
        raise HTTPException(status_code=404, detail="Code not found")
    app.extra['bto_ir_cmd'].transmit(db_code.code_str)
    file_path = app.extra['camera_cmd'].run()
    label, _ = app.extra['predictor'].predict(file_path)
    return label


@app.delete('/codes/{code_key}')
def delete_code(code_key: str, db: Session = Depends(get_db)):
    db_code = crud.get_code_by_key(db, key=code_key)
    if db_code is None:
        raise HTTPException(status_code=404, detail="Code not found")
    return crud.delete_code(db=db, key=code_key)
