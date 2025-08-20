from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from library import Library, fetch_book_from_api
from book import Book

app = FastAPI()
library = Library()


class ISBNRequest(BaseModel):
    isbn: str


@app.get("/books")
def list_books():
    return [book.to_dict() for book in library.list_books()]


@app.post("/books")
def add_book_api(request: ISBNRequest):
    if library.find_book(request.isbn):
        raise HTTPException(status_code=400, detail="Bu ISBN zaten mevcut.")

    book = fetch_book_from_api(request.isbn)
    if not book:
        raise HTTPException(status_code=404, detail="Kitap bulunamadı veya API hatası.")

    library.add_book(book)
    return book.to_dict()


@app.delete("/books/{isbn}")
def remove_book_api(isbn: str):
    if not library.find_book(isbn):
        raise HTTPException(status_code=404, detail="Kitap bulunamadı.")

    library.remove_book(isbn)
    return {"message": f"Book with ISBN {isbn} has been deleted."}
