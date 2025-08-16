import json
import os
import httpx
from book import Book


class Library:
    def __init__(self, json_file="library.json"):
        self.json_file = json_file
        self.books = []
        self.load_books()

    def load_books(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as f:
                try:
                    data = json.load(f)
                    self.books = [Book(**item) for item in data]
                except (json.JSONDecodeError, FileNotFoundError):
                    self.books = []
        else:
            self.books = []

    def save_books(self):
        data = [{'title': book.title, 'author': book.author, 'isbn': book.isbn} for book in self.books]
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def add_book(self, isbn):
        if self.find_book(isbn):
            print(f"Hata: {isbn} ISBN numaralı kitap zaten kütüphanede mevcut.")
            return

        print("Kitap bilgileri aranıyor...")

        try:
            url = f"https://openlibrary.org/isbn/{isbn}.json"
            response = httpx.get(url, timeout=10, follow_redirects=True)
            response.raise_for_status()
            data = response.json()

            title = data.get('title')

            authors_data = data.get('authors', [])
            author_names = []

            for author_info in authors_data:
                author_key = author_info.get('key')
                if author_key:
                    try:
                        author_url = f"https://openlibrary.org{author_key}.json"
                        author_response = httpx.get(author_url, timeout=10, follow_redirects=True)
                        author_response.raise_for_status()
                        author_data = author_response.json()
                        author_name = author_data.get('name')
                        if author_name:
                            author_names.append(author_name)
                    except httpx.HTTPStatusError:
                        continue
                    except httpx.RequestError:
                        continue

            author = ", ".join(author_names) if author_names else "Bilinmiyor"

            if title:
                new_book = Book(title, author, isbn)
                self.books.append(new_book)
                self.save_books()
                print(f"'{title}' kütüphaneye başarıyla eklendi.")
            else:
                print("Hata: API'den gerekli kitap bilgileri (başlık) alınamadı.")

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                print(f"Hata: {isbn} ISBN numaralı kitap bulunamadı.")
            else:
                print(f"HTTP Hatası: {e}")
        except httpx.RequestError as e:
            print(f"Bir hata oluştu: API'ye bağlanılamadı. {e}")
        except Exception as e:
            print(f"Beklenmeyen bir hata oluştu: {e}")

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def remove_book(self, isbn):
        book_to_remove = self.find_book(isbn)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
            print(f"ISBN numaralı kitap '{isbn}' silindi.")
        else:
            print(f"Hata: '{isbn}' ISBN numaralı kitap bulunamadı.")

    def list_books(self):
        if not self.books:
            print("Kütüphanede hiç kitap yok.")
            return []
        print("\n--- Kütüphanedeki Kitaplar ---")
        for book in self.books:
            print(book)
        return self.books