from fastapi import FastAPI,Depends
import uvicorn 
from pydantic import BaseSettings
from database import engine
import models
from routers.auth import SQLAlchemyError,sqlalchemy_exception_handler
from routers.todos import NegativeNumberException,negative_number_exception_handler
from routers import auth,todos,users
from external_routers import company,dependencies


import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


#DEACTIVATE DOCUMENTATION (REDOC AND SWAGGER UI)
class Settings(BaseSettings):
    docs_url: str = ""
    redoc_url:str=""


settings = Settings()

app = FastAPI(redoc_url=settings.docs_url,
# docs_url=settings.docs_url
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(users.router)
app.include_router(company.router,
  prefix="/company",
    tags=["company"],
    dependencies=[Depends(dependencies.get_token_header)],
    responses={401:{"user":"Not Authorized"}}
)

app.add_exception_handler(SQLAlchemyError,sqlalchemy_exception_handler)
app.add_exception_handler(NegativeNumberException,negative_number_exception_handler)


#SCRIPT TO RUN UVICORN MORE EASIER WITH python uvicorn 
if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", host=os.getenv("HOST"), reload=True, port=int(os.getenv("PORT")))