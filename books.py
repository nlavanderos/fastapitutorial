from fastapi import FastAPI
from enum import Enum

app = FastAPI()


BOOKS= {
    'books_1':{'title':'Title One', 'author':'Author One'},
    'books_2':{'title':'Title Two', 'author':'Author Two'}, 
    'books_3':{'title':'Title Three', 'author':'Author Three'}, 
    'books_4':{'title':'Title Four', 'author':'Author Four'}, 
    'books_5':{'title':'Title Five', 'author':'Author Five'}, 

}


class DirectionName(str, Enum):
    n:str="North"
    s:str="South"
    e:str="East"
    w:str="West"

# We use async in FastAPI, due to asynchronous code, concurrency, and parallelism.



#DELETE REQUEST BELOW

@app.delete("/delete_book/{book_name}")
async def delete(book_name:str|None=None):
    if book_name:
        del BOOKS[book_name]
        return f'Book {book_name} is deleted'
    
    return f'{book_name} is deleted'





#PUT REQUEST BELOW

@app.put("/{book_name}")
async def update_book(book_name:str,book_title:str,book_author:str):
    book_info={"title":book_title,"author":book_author}
    BOOKS[book_name]=book_info
    return book_info

# POST REQUEST BELOW

@app.post("/add")
async def create_book(book_title:str,book_author:str):

    index=1
    if len(BOOKS)>0:
        for book in BOOKS:
            idx=int(book.split('_')[-1])
            #Resolve the gaps betweens elements
            if (idx >=index):
                index=idx
            else:
                index=index+1
                BOOKS[f'book_{index}']={'title':book_title, 'author':book_author}
                return BOOKS[f'book_{index}']
            
    BOOKS[f'book_{index+1}']={'title':book_title, 'author':book_author}
    return BOOKS[f'book_{index+1}']


# GET METHODS BELOW

@app.get("/")
async def read_all_books():
    return BOOKS


@app.get("/exclude_book/{book_name}")
async def delete(book_name:str|None=None):
    if book_name:
        new_books=BOOKS.copy()
        del new_books[book_name]
        return new_books
    
    return BOOKS


@app.get("/directions/{directions_name}")
async def get_direction(directions_name: DirectionName):
    if directions_name == DirectionName.n:
        return {"Direction":directions_name,"sub":"UPSIDE"}
    if directions_name == DirectionName.s:
        return {"Direction":directions_name,"sub":"DOWNSIDE"}
    if directions_name == DirectionName.w:
        return {"Direction":directions_name,"sub":"LEFTSIDE"}

    return {"Direction":directions_name,"sub":"RIGHTSIDE"}


@app.get("/books/{book_name_title}")
async def get_title_book(book_name_title:str):

    return  BOOKS[book_name_title]['title']



@app.get("/books/{book_name}")
async def read_book(book_name:str):

    return BOOKS[book_name]