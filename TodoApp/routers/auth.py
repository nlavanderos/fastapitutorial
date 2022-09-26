import sys
sys.path.append("..")


from fastapi import Depends,Request,HTTPException,status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt,JWTError
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from pydantic import BaseSettings

from database import engine,SessionLocal

import models
from schemas import CreateUser
from passlib.context import CryptContext




bcrypt_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

# openssl rand -hex 32 in linux
SECRET_KEY="834e8dc5f8cbc05f30c1893aec0e69c5c9b75abfeff9a9b4af40ca2a9043e91c"
ALGORITHM="HS256"

#DEACTIVATE DOCUMENTATION (REDOC AND SWAGGER UI)
class Settings(BaseSettings):
    docs_url: str = ""
    redoc_url:str=""


settings = Settings()

# app = FastAPI(redoc_url=settings.docs_url,
# # docs_url=settings.docs_url
# )

router=APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={401:{"user":"Not Authorized"}}

)


models.Base.metadata.create_all(bind=engine)
oauth2_bearer=OAuth2PasswordBearer(tokenUrl="token")

class SQLAlchemyError(Exception):
    def __init__(self,error):
        self.error=error


def sqlalchemy_exception_handler(request: Request ,exception:SQLAlchemyError):
    return JSONResponse(status_code=419,
    content={"message":f"{exception.error}..."})


def get_session():
    try:
        db:Session=SessionLocal()
        yield db
    finally:
        db.close

def get_password_hash(password):
    return bcrypt_context.hash(password)


def verify_password(password,hashed_password):
    return bcrypt_context.verify(password,hashed_password)

def authenticate_user(username:str,password:str,db):
    user=db.query(models.Users)\
        .filter(models.Users.username==username)\
        .first()
    if not user:
        return False
    if not verify_password(password,user.hashed_password):
        return False
    return user
    


def create_access_token(username:str,user_id:int,expires_delta:timedelta|None=None):

    encode={"sub":username,"id":user_id}

    if expires_delta:
        expire=datetime.utcnow()+expires_delta
    else:
        expire=datetime.utcnow()+timedelta(minutes=15)
    encode.update({"exp":expire})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

@router.post("/create/user")
async def  create_new_user(create_user:CreateUser,db:Session=Depends(get_session)):
    try:
        create_user_model=models.Users()

        create_user_model.username=create_user.username
        create_user_model.first_name=create_user.first_name
        create_user_model.email=create_user.email
        create_user_model.last_name=create_user.last_name
        create_user_model.hashed_password=get_password_hash(create_user.password)
        create_user_model.is_active=True

        db.add(create_user_model)
        db.commit()

        return JSONResponse(content={"msg":"User created","transaction":"Succesfull"},status_code=200)
    except IntegrityError as e:
        raise SQLAlchemyError(error=f"la excepcion fue {e.args[0]}, el problema fue {e.orig}")

@router.post("/token")
async def login_for_access_token(form_data:OAuth2PasswordRequestForm=Depends(),
                                db:Session=Depends(get_session)):
    user=authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise token_exception()

    token_expires=timedelta(minutes=20)
    token=create_access_token(user.username,user.id,expires_delta=token_expires)
    return {"token":token}



# DECODE
async def get_current_user(token:str=Depends(oauth2_bearer)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get("sub")
        user_id:int=payload.get("id")
        if username is None or user_id is None:
            raise get_user_exception()
        return {"username":username,"id":user_id}
    except JWTError:
        raise get_user_exception()


def get_user_exception():
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"},
    )
    return credentials_exception

def token_exception():
    token_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="incorrect username or password",
        headers={"WWW-Authenticate":"Bearer"},
    )
    return token_exception  
