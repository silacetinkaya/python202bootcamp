import json
import os
from book import Book
import httpx


def fetch_book_from_api(isbn: str) -> Book | None:
    """ISBN ile OpenLibrary API'den kitap bilgisi çeker ve Book nesnesi döner."""
    url = f"https://openlibrary.org/isbn/{isbn}.json"
    try:
        response = httpx.get(url, follow_redirects=True, timeout=10)
        response.raise_for_status()
        data = response.json()

        title = data.get("title", "Bilinmiyor")
        authors = data.get("authors", [])
        author_name = "Bilinmiyor"

        if authors:
            author_key = authors[0].get("key")
            if author_key:
                author_url = f"https://openlibrary.org{author_key}.json"
                author_response = httpx.get(author_url, follow_redirects=True, timeout=10)
                author_response.raise_for_status()
                author_data = author_response.json()
                author_name = author_data.get("name", "Bilinmiyor")

        return Book(title, author_name, isbn)

    except httpx.HTTPStatusError:
        print("Kitap bulunamadı. ISBN yanlış olabilir.")
    except httpx.RequestError:
        print("Ağ hatası. İnternet bağlantınızı kontrol edin.")
    except Exception as e:
        print(f"Beklenmeyen hata: {e}")

    return None


class Library:
    def __init__(self, json_file: str = "library.json"):
        self.json_file = json_file
        self.books: list[Book] = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.books = [Book(**item) for item in data]
            except json.JSONDecodeError:
                self.books = []
        else:
            self.books = []

    def save_books(self):
        data = [book.to_dict() for book in self.books]
        with open(self.json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_book(self, book: Book):
        if self.find_book(book.isbn):
            print("Bu ISBN zaten mevcut.")
            return None
        self.books.append(book)
        self.save_books()
        print(f"Kitap eklendi: {book}")
        return book

    def find_book(self, isbn: str) -> Book | None:
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def remove_book(self, isbn: str) -> bool:
        book_to_remove = self.find_book(isbn)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
            print(f"ISBN numaralı kitap '{isbn}' silindi.")
            return True
        else:
            print(f"Hata: '{isbn}' ISBN numaralı kitap bulunamadı.")
            return False

    def list_books(self) -> list[Book]:
        return self.books
