import sys
sys.path.append("..")

from fastapi import Depends,HTTPException,Request,status,Header,APIRouter
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from typing import List
from pydantic import BaseSettings

from database import engine,SessionLocal
from schemas import TitleAndDescription,WithoutId
import models

from .auth import get_current_user,get_user_exception



#DEACTIVATE DOCUMENTATION (REDOC AND SWAGGER UI)
class Settings(BaseSettings):
    docs_url: str = ""
    redoc_url:str=""


settings = Settings()

router=APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={401:{"user":"Not Authorized"}}

)

models.Base.metadata.create_all(bind=engine)


class NegativeNumberException(Exception):
    def __init__(self,id):
        self.id=id


def negative_number_exception_handler(request: Request ,exception:NegativeNumberException):
    return JSONResponse(status_code=404,
    content={"message":f"Porque necesitas ese id {exception.id}..."
                        f"Estas bien???"})

def get_session():
    try:
        db:Session=SessionLocal()
        yield db
    finally:
        db.close


@router.get("/user")
async def read_all_by_user(user:dict=Depends(get_current_user),db:Session=Depends(get_session)):
    if user is None:
        raise get_user_exception()
    return db.query(models.Todos).\
    filter(models.Todos.owner_id == user.get("id")).\
    all()


@router.post("/login",status_code=status.HTTP_200_OK)
async def login(user:str|None=Header(),password:str|None=Header(),db:Session=Depends(get_session)):  
    if user=="admin" and password=="123456":
        return db.query(models.Todos).all()
    return "Invalid credentials"



@router.get('/title-info',response_model=List[TitleAndDescription])
async def read_basics(db:Session=Depends(get_session)):
    return db.query(models.Todos).all()



@router.get('/')
async def read_all(db:Session=Depends(get_session)):
    return db.query(models.Todos).all()




@router.get("/{todo_id}")
async def read_todo_by_id(todo_id:int,user:dict=Depends(get_current_user),db:Session=Depends(get_session)):

    if user is None:
        raise get_user_exception()
    todo_model=db.query(models.Todos).\
    filter(models.Todos.id==todo_id).\
    filter(models.Todos.owner_id==user.get("id")).\
    first()

    if todo_model is not None:
    
        return todo_model
    
    raise NegativeNumberException(id=todo_id)

@router.post("/create_todo")
async def create_todo(todo:WithoutId,user:dict=Depends(get_current_user),db:Session=Depends(get_session)):
    if user is None:
        raise get_user_exception()
    todo_model=models.Todos()
    todo_model.completed=todo.completed
    todo_model.description=todo.description
    todo_model.priority=todo.priority
    todo_model.title=todo.title
    todo_model.owner_id=user.get("id")

    db.add(todo_model)
    db.commit()

    return JSONResponse(content={"msg":"created","transaction":"Succesfull"},status_code=200)

@router.put("/update_todo")
async def update_todo(id_todo:int,todo:WithoutId,user:dict=Depends(get_current_user),db:Session=Depends(get_session)):
    if user is None:
        raise get_user_exception()
    todo_model=db.query(models.Todos).\
    filter(models.Todos.id==id_todo).\
    filter(models.Todos.owner_id==user.get("id")).\
    first()    

    if(todo_model is None):
        raise NegativeNumberException

    todo_model.completed=todo.completed
    todo_model.description=todo.description
    todo_model.priority=todo.priority
    todo_model.title=todo.title

    db.add(todo_model)
    db.commit()

    return JSONResponse(content={"msg":"updated","transaction":"Succesfull"},status_code=200)


@router.delete("/delete_todo")
async def delete_todo(id_todo:int,user:dict=Depends(get_current_user),db:Session=Depends(get_session)):
    if user is None:
        raise get_user_exception()
    base=db.query(models.Todos).\
    filter(models.Todos.id==id_todo).\
    filter(models.Todos.owner_id==user.get("id"))

    todo_model=base.first()

    if(todo_model is None):
        raise NegativeNumberException
    
    base.delete()
    db.commit()

    return JSONResponse(content={"msg":"deleted","transaction":"Succesfull"},status_code=200)




def http_exception():
    return HTTPException(status_code=404, detail="Not found")
