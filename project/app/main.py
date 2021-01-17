from datetime import datetime, timedelta
from typing import List
from typing import Optional
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, status, File, UploadFile, Response
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import schemas
from database import SessionLocal, engine
import crud
import models
from config import TOKEN_URL, SECRET_KEY, ALGORITHM
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

FAIL = False

origins = [
    "http://localhost",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = str(payload.get("sub"))
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


@app.get("/v1/get_services/", response_model=List[int])
async def create_upload_file(username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return [service.id for service in crud.get_services(db, username)]


@app.get("/v1/get_service/")
async def create_upload_file(service_id: int, username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    service = crud.get_service(db, username, service_id)
    if service:
        return Response(service.service)


@app.delete("/v1/get_service/")
async def create_upload_file(service_id: int, username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    service = crud.delete_service(db, username, service_id)
    if service:
        return Response(service.service)
    return {"error": "Could not access the service."}


@app.get("/v1/add_allowed_user/", response_model=dict)
async def create_upload_file(service_id: int, add_user: str, username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    success = crud.try_add_allowed_user(db, add_user, service_id, username)
    return {"success": success}


@app.post("/v1/upload_service/", response_model=dict)
async def create_upload_file(file: UploadFile = File(...), username: str = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    contents = await file.read()
    service = crud.create_service(db=db, user=username, file=contents, service_name=file.filename)
    return {"id": service.id, "owner": service.owner}


@app.get("/v1/health/live_check", response_model=str)
async def live_check():
    return "OK"


@app.get("/v1/health/test_crash", response_model=str)
async def set_fail():
    global FAIL
    FAIL = True
    return "OK"


@app.get("/v1/health/db_ready", response_model=dict)
async def test_db(db: Session = Depends(get_db)):
    global FAIL
    if FAIL:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Intentional fail",
        )
    service = bytes(b"random service")
    username = str(uuid4())
    new_service = crud.create_service(db=db, user=username, file=service, service_name="test.txt")
    if not new_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to create new service",
        )
    print(new_service.id)
    get_service_ret = crud.get_service(db, new_service.owner, new_service.id)
    if not get_service_ret or get_service_ret.owner != username:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to get new service",
        )
    del_new_user = crud.delete_service(db, new_service.owner, new_service.id)
    if not del_new_user:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to delete new service",
        )
    return {"database_check": "ok"}
