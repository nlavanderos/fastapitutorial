from fastapi import FastAPI,Depends,HTTPException,Request,status,Header
import uvicorn 
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session

from typing import List
from pydantic import BaseSettings

from database import engine,SessionLocal
from schemas import TitleAndDescription,WithoutId
import models




#DEACTIVATE DOCUMENTATION (REDOC AND SWAGGER UI)
class Settings(BaseSettings):
    docs_url: str = ""
    redoc_url:str=""


settings = Settings()

app = FastAPI(redoc_url=settings.docs_url,
# docs_url=settings.docs_url
)

models.Base.metadata.create_all(bind=engine)


class NegativeNumberException(Exception):
    def __init__(self,id):
        self.id=id

@app.exception_handler(NegativeNumberException)
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


@app.post("/login",status_code=status.HTTP_200_OK)
async def login(user:str|None=Header(),password:str|None=Header(),db:Session=Depends(get_session)):  
    if user=="admin" and password=="123456":
        return db.query(models.Todos).all()
    return "Invalid credentials"



@app.get('/title-info',response_model=List[TitleAndDescription])
async def read_basics(db:Session=Depends(get_session)):
    return db.query(models.Todos).all()



@app.get('/')
async def read_all(db:Session=Depends(get_session)):
    return db.query(models.Todos).all()




@app.get("/todo/{todo_id}")
async def read_todo_by_id(todo_id:int,db:Session=Depends(get_session)):
    todo_model=db.query(models.Todos).\
    filter(models.Todos.id==todo_id).\
    first()

    if todo_model is not None:
    
        return todo_model
    
    raise NegativeNumberException(id=todo_id)

@app.post("/create_todo")
async def create_todo(todo:WithoutId,db:Session=Depends(get_session)):
    todo_model=models.Todos()
    todo_model.completed=todo.completed
    todo_model.description=todo.description
    todo_model.priority=todo.priority
    todo_model.title=todo.title

    db.add(todo_model)
    db.commit()

    return JSONResponse(content={"msg":"created","transaction":"Succesfull"},status_code=200)

@app.put("/update_todo")
async def update_todo(id_todo:int,todo:WithoutId,db:Session=Depends(get_session)):

    todo_model=db.query(models.Todos).\
    filter(models.Todos.id==id_todo).\
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


@app.delete("/delete_todo")
async def delete_todo(id_todo:int,db:Session=Depends(get_session)):

    base=db.query(models.Todos).\
    filter(models.Todos.id==id_todo)

    todo_model=base.first()

    if(todo_model is None):
        raise NegativeNumberException
    
    base.delete()
    db.commit()

    return JSONResponse(content={"msg":"deleted","transaction":"Succesfull"},status_code=200)




def http_exception():
    return HTTPException(status_code=404, detail="Not found")

#SCRIPT TO RUN UVICORN MORE EASIER WITH python uvicorn 
if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", host="localhost", reload=True, port=8081)