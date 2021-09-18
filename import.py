import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import csv
import env

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

book = open("books.csv")
books = csv.reader(book)
print (books) 
i = 0

for isbn, title, author, year in books :
    if isbn == "isbn": 
        print ("Nos hemos saltado la primera linea");
    else: 
        i = i+1
        db.execute("Insert into books (isbn, title, author, year) values(:isbn, :title, :author, :year)", {"isbn": isbn, "title": title, "author":author, "year":year} )
        print(f"Este es el libro numero {i}")
    db.commit()