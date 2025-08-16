from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from library import Library


# Pydantic ile veri modeli oluşturma
class BookModel(BaseModel):
    title: str
    author: str
    isbn: str


app = FastAPI()
library = Library()


@app.get("/books")
def list_books():
    """Kütüphanedeki tüm kitapları listeler."""
    return library.books


@app.post("/books")
def add_book_api(book: BookModel):
    """Yeni bir kitabı kütüphaneye ekler."""
    if library.find_book(book.isbn):
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists.")

    new_book = library.add_book(book)
    return new_book


@app.delete("/books/{isbn}")
def remove_book_api(isbn: str):
    """Belirtilen ISBN'e sahip kitabı kütüphaneden siler."""
    if not library.find_book(isbn):
        raise HTTPException(status_code=404, detail="Book not found.")

    library.remove_book(isbn)
    return {"message": f"Book with ISBN: {isbn} has been deleted."}