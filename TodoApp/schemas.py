from pydantic import BaseModel


# SET ORM MODE TO RETURN DATA, DEFAULT MODE TO AN DATABASE IS RETURN A DICT
class OurBaseModel(BaseModel):
    class Config:
        orm_mode = True

# FOR SHOW DATA
class TitleAndDescription(OurBaseModel):
    id:int
    title:str
    description:str|None=None

# FOR CREATE ROW IN BD
class WithoutId(OurBaseModel):
    title:str
    description:str|None=None
    priority:int
    completed:bool


class CreateUser(OurBaseModel):
    username:str
    email:str|None=None
    first_name:str
    last_name:str
    password:str