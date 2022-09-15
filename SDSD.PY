from collections import OrderedDict

BOOKS= {
    'books_1':{'title':'Title One', 'author':'Author One'},
    'books_2':{'title':'Title Two', 'author':'Author Two'}, 
    'books_3':{'title':'Title Three', 'author':'Author Three'}, 
    'books_6':{'title':'Title Six', 'author':'Author Four'}, 
    'books_5':{'title':'Title Five', 'author':'Author Five'}, 

}


BOOKS=dict(sorted(BOOKS.items(),key=lambda x:x[0]))


print(BOOKS)