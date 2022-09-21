from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, BaseSettings
from uuid import UUID, uuid1
from starlette.responses import JSONResponse
from requests import Request
import uvicorn

BOOKS = []

#DEACTIVATE DOCUMENTATION (REDOC AND SWAGGER UI)
class Settings(BaseSettings):
    docs_url: str = ""
    redoc_url:str=""


settings = Settings()

app = FastAPI(redoc_url=settings.docs_url,docs_url=settings.docs_url)



class NegativeNumberException(Exception):
    def __init__(self,books_to_return):
        self.books_to_return = books_to_return

@app.exception_handler(NegativeNumberException)
def negative_number_exception_handler(request: Request ,exception:NegativeNumberException):

    return JSONResponse(status_code=418,
    content={"message":f"Porque necesitas {exception.books_to_return} libros..."
                        f"Estas bien???"})


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description: str | None = Field(
        title="Description of the book", max_length=100, min_length=1)
        # greather than and low than
    ratio: int=Field(gt=1,lt=101)

    class Config:
        schema_extra={
            "example":{
            "id":str(uuid1()),
            "title":"Naruto",
            "author":"Kishimoto",
            "description":"Ninja world",
            "ratio":66
            }
        }

# uuid1 is generated my mac addres
# uuid4 is random 

def create_book_noapi():
    new_book=Book(id=str(uuid1()),title="Description of the book",author="asas",description="asdsad",ratio=12)
    new_book2=Book(id= str(uuid1()),title="Description of the book",author="asas",description="asdsad",ratio=51)
    new_book3=Book(id= "33385f38-3802-11ed-9127-00e04c6f9131",title="SADA of the book",author="ASD",description="asdsad",ratio=21)
   
    BOOKS.append(new_book)
    BOOKS.append(new_book2)
    BOOKS.append(new_book3)



@app.post('/')
async def create_book(book: Book):
 
    BOOKS.append(book)
    return book


@app.get('/')
async def get_books(books_to_return:int | None):
    if   books_to_return<0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        create_book_noapi()
    if len(BOOKS) >= books_to_return>0:
        i=0
        new_books=[]
        while(i!=books_to_return):
            new_books.append(BOOKS[i])
            i+=1
        return new_books
    return BOOKS


@app.get("/book/{by_uuid}")
async def get_info_by_uuid(by_uuid:UUID):
    for x in BOOKS:
        if(x.id==by_uuid):
            return x


@app.delete("/book/{book_name}")
async def delete(book_id: UUID | None = None):
    '''DELETE THE BOOK OF THE BOOKS LIST'''

    for x in BOOKS:
        if(x.id==book_id):
            del x
            return f'Book_id {book_id} is deleted'

    raise raise_error_exception()
    # return f'{book_id} is not in the format'



@app.put("/book/{book_upd_id}")
async def update_book(book_upd_id: UUID,book:Book):
    '''UPDATE THE INFO OF THE BOOK'''
    cont=0
    for x in BOOKS:
        
        if(x.id==book_upd_id):
            BOOKS[cont] = book
            return BOOKS[cont]
        cont+=1
    return f'BOOK ID {book_upd_id} NOT FOUND'


def raise_error_exception():
    return HTTPException(status_code=404,detail="uid not found",headers={"X-Header-Error":"not found"})


#SCRIPT TO RUN UVICORN MORE EASIER WITH python uvicorn 
if __name__ == "__main__":
    uvicorn.run(f"{__name__}:app", host="localhost", reload=True, port=8081)