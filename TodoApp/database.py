from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from pathlib import Path
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)



SQLALCHEMY_DATABASE_URL=os.getenv("SQLALCHEMY_DATABASE_URL")
PG_DATABASE_URL=os.getenv("PG_DATABASE_URL")
# DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}
# engine=create_engine("sqlite:///./todos.db", connect_args={"check_same_thread": False})
engine=create_engine(PG_DATABASE_URL)
SessionLocal= sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()