#standard library
from enum import Enum
#third party libraries
from fastapi import FastAPI
#local libraries

# We use async in FastAPI, due to asynchronous code, concurrency, and parallelism.
app = FastAPI()


BOOKS = {
    'books_1': {'title': 'Title One', 'author': 'Author One'},
    'books_2': {'title': 'Title Two', 'author': 'Author Two'},
    'books_3': {'title': 'Title Three', 'author': 'Author Three'},
    'books_4': {'title': 'Title Four', 'author': 'Author Four'},
    'books_5': {'title': 'Title Five', 'author': 'Author Five'},

}


class DirectionName(str, Enum):
    '''ENUM ALLOW TO SELECT DATA IN FASTAPI'''
    n: str = "North"
    s: str = "South"
    e: str = "East"
    w: str = "West"


# DELETE REQUEST BELOW

@app.delete("/delete_book/{book_name}")
async def delete(book_name: str | None = None):
    '''DELETE THE BOOK OF THE BOOKS LIST'''
    if book_name.split('_')[0]=='books':
        del BOOKS[book_name]
        return f'Book {book_name} is deleted'
    else:
        return f'{book_name} is not in the format'


# PUT REQUEST BELOW

@app.put("/{book_name}")
async def update_book(book_name: str, book_title: str, book_author: str):
    '''UPDATE THE INFO OF THE BOOK'''
    book_info = {"title": book_title, "author": book_author}
    BOOKS[book_name] = book_info
    return book_info



# POST REQUEST BELOW


@app.post("/add")
async def create_book(book_title: str, book_author: str):
    '''CREATE BOOK IN THE LIST OF BOOKS'''
    global BOOKS
    index = 1
    if len(BOOKS) > 0:

        for book in BOOKS:
            idx = int(book.split('_')[-1])
            # Resolve the gaps betweens elements
            if (index-idx):
                BOOKS[f'books_{index}'] = {
                    'title': book_title, 'author': book_author}
                BOOKS = dict(sorted(BOOKS.items(), key=lambda x: x[0]))

                return BOOKS[f'books_{index}']
            else:
                index += 1

            # IN ORDER
        BOOKS[f'books_{index}'] = {'title': book_title, 'author': book_author}
        BOOKS = dict(sorted(BOOKS.items(), key=lambda x: x[0]))
        return BOOKS[f'books_{index}']


# GET METHODS BELOW


@app.get("/")
async def read_all_books():
    
    '''READ ALL CONTENT OF THE OBJECT BOOK'''   
    return BOOKS


@app.get("/exclude_book/{book_name}")
async def delete(book_name: str | None = None):
    '''PRINT ALL BOOKS MINUS THE BOOK INSERTED''' 
    if book_name:
        new_books = BOOKS.copy()
        del new_books[book_name]
        return new_books

    return BOOKS


@app.get("/directions/{directions_name}")
async def get_direction(directions_name: DirectionName):

    ''' SELECT VALUE AND MATCH WITH THE DIRECTION CLASS VALUES , GENERATE NEW OBJECT'''

    if directions_name == DirectionName.n:
        return {"Direction": directions_name, "sub": "UPSIDE"}
    if directions_name == DirectionName.s:
        return {"Direction": directions_name, "sub": "DOWNSIDE"}
    if directions_name == DirectionName.w:
        return {"Direction": directions_name, "sub": "LEFTSIDE"}

    return {"Direction": directions_name, "sub": "RIGHTSIDE"}


@app.get("/books/{book_name_title}")
async def get_title_book(book_name_title: str):
    '''GET THE TITLE OF THE BOOK'''
    return BOOKS[book_name_title]['title']


# query params get
@app.get("/readbook/")
async def read_book(book_name: str):
    ''' GET DATA OF THE BOOK'''
    return BOOKS[book_name]