from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from library import Library
from book import Book
import httpx


# Pydantic ile veri modeli oluşturma
class BookModel(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str


app = FastAPI()
library = Library()


@app.get("/books")
def list_books():
    """Kütüphanedeki tüm kitapları listeler."""
    return library.list_books()


@app.post("/books")
def add_book_api(book: BookModel):
    """Yeni bir kitabı kütüphaneye ekler."""
    if library.find_book(book.isbn):
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists.")

    print("Kitap bilgileri aranıyor...")
    url = f"https://openlibrary.org/isbn/{book.isbn}.json"

    try:
        response = httpx.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        title = data.get('title')
        authors_data = data.get('authors', [])
        author = ", ".join(
            [httpx.get(f"https://openlibrary.org{auth['key']}.json").json().get('name', 'Bilinmiyor') for auth in
             authors_data])

        if not title or not author:
            raise HTTPException(status_code=404, detail="API'den gerekli kitap bilgileri (başlık/yazar) alınamadı.")

        new_book = Book(title, author, book.isbn)
        library.add_book(new_book)
        return new_book

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"ISBN numaralı kitap bulunamadı.")
        else:
            raise HTTPException(status_code=e.response.status_code, detail=f"HTTP Hatası: {e}")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Bir hata oluştu: API'ye bağlanılamadı.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Beklenmeyen bir hata oluştu: {e}")


@app.delete("/books/{isbn}")
def remove_book_api(isbn: str):
    """Belirtilen ISBN'e sahip kitabı kütüphaneden siler."""
    if not library.find_book(isbn):
        raise HTTPException(status_code=404, detail="Book not found.")

    library.remove_book(isbn)
    return {"message": f"Book with ISBN: {isbn} has been deleted."}