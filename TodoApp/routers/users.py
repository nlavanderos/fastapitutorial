import sys
sys.path.append("..")


from fastapi import Depends,APIRouter
from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models
from .auth import get_current_user,get_user_exception,verify_password,get_password_hash
from schemas import UserVerification

router=APIRouter(
    prefix="/users",
    tags=["users"],
    responses={401:{"user":"Not Authorized"}}

)


models.Base.metadata.create_all(bind=engine)


def get_session():
    try:
        db:Session=SessionLocal()
        yield db
    finally:
        db.close

@router.get("/")
async def get_users(db:Session=Depends(get_session)):
    return db.query(models.Users).all()



@router.get("/{user_id}")
async def user_by_path(user_id:int,db:Session=Depends(get_session)):
    user_model=db.query(models.Users).\
        filter(models.Users.id==user_id).\
        first()
    if user_model is not None:
        return user_model
    return "Invalid user_id"


@router.get("/by_query")
async def user_by_query(user_id:int,db:Session=Depends(get_session)):
    user_model=db.query(models.Users).\
        filter(models.Users.id==user_id).\
        first()
    if user_model is not None:
        return user_model

@router.put("/password")
async def user_password_change(user_verification:UserVerification,user:dict=Depends(get_current_user) ,db:Session=Depends(get_session)):
    
    if user is None:
        raise get_user_exception()

    user_model=db.query(models.Users).\
        filter(models.Users.id==user.get("id")).\
        first()
    

    if user_model is not None:
        if user_verification.username==user_model.username and verify_password(user_verification.password,user_model.hashed_password):
            user_model.hashed_password=get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return "Succesfull"
    return "Invalid user or request"


@router.delete("/delete")
async def user_delete(user:dict=Depends(get_current_user) ,db:Session=Depends(get_session)):

    if user is None:
        raise get_user_exception()
    
    user_model = db.query(models.Users).\
        filter(models.Users.id==user.get("id")).\
        first()

    if user_model is None:
        return "Invalid user or request"
    

    db.query(models.Users).\
        filter(models.Users.id==user.get("id")).\
        delete()

    db.commit()

    return "Delete successful"