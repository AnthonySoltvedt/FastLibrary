from typing import List
from itertools import count
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette import status


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    available: bool


class Book(BookBase):
    id: int


class Member(BaseModel):
    id: int
    name: str
    email: str


app = FastAPI()
books: List[Book] = []
members_list: List[Member] = []

id_counter = count(1)
member_id_counter = count(1)


@app.get("/")
def index():
    return {"message": "Hello World!"}


# ------------------------
# BOOKS
# ------------------------
@app.get("/books", response_model=List[Book])
def get_books():
    return books


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def add_a_new_book(book: BookBase):
    new_book = Book(id=next(id_counter), **book.dict())
    books.append(new_book)
    return new_book


@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    for b in books:
        if b.id == book_id:
            return b
    raise HTTPException(status_code=404, detail="Book not found")


@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: BookBase):
    for i, b in enumerate(books):
        if b.id == book_id:
            books[i] = Book(id=book_id, **updated_book.dict())
            return books[i]
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int):
    for b in books:
        if b.id == book_id:
            books.remove(b)
            return
    raise HTTPException(status_code=404, detail="Book not found")


# ------------------------
# MEMBERS
# ------------------------
@app.get("/members", response_model=List[Member])
def list_members():
    return members_list


@app.post("/members", response_model=Member, status_code=status.HTTP_201_CREATED)
def add_member(member: Member):
    member.id = next(member_id_counter)
    members_list.append(member)
    return member


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
