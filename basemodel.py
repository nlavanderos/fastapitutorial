from sys import prefix
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID, uuid1


BOOKS = []

app = FastAPI()


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
            "desc":"Ninja world",
            "ratio":66
            }
        }

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


@app.get('/')
async def get_books(books_to_return:int | None):
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
    counter=0
    for x in BOOKS:
        counter+=1
        if(x.id==book_id):
            del x
            return f'Book_id {book_id} is deleted'

    return f'{book_id} is not in the format'



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