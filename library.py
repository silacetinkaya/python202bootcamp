import json
import os
import httpx  # Yeni eklenen kütüphane
from book import Book


class Library:
    def __init__(self, json_file="library.json"):
        self.json_file = json_file
        self.books = []
        self.load_books()

    def load_books(self):
        """Uygulama başladığında library.json dosyasından kitapları yükler."""
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
        """Kütüphanede bir değişiklik olduğunda (ekleme/silme) tüm kitap listesini library.json dosyasına yazar."""
        data = [{'title': book.title, 'author': book.author, 'isbn': book.isbn} for book in self.books]
        with open(self.json_file, 'w') as f:
            json.dump(data, f, indent=4)

    def add_book(self, isbn):
        """ISBN numarasıyla harici API'den kitap bilgilerini çekerek kütüphaneye ekler."""
        if self.find_book(isbn):
            print(f"Hata: {isbn} ISBN numaralı kitap zaten kütüphanede mevcut.")
            return

        print("Kitap bilgileri aranıyor...")
        url = f"https://openlibrary.org/isbn/{isbn}.json"

        try:
            response = httpx.get(url, timeout=10)
            response.raise_for_status()  # HTTP hataları için hata fırlatır (örn: 404)
            data = response.json()

            title = data.get('title')
            authors_data = data.get('authors', [])
            author = ", ".join(
                [httpx.get(f"https://openlibrary.org{auth['key']}.json").json().get('name', 'Bilinmiyor') for auth in
                 authors_data])

            if title and author:
                new_book = Book(title, author, isbn)
                self.books.append(new_book)
                self.save_books()
                print(f"'{title}' kütüphaneye başarıyla eklendi.")
            else:
                print("Hata: API'den gerekli kitap bilgileri (başlık/yazar) alınamadı.")

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
        """ISBN ile belirli bir kitabı bulur ve Book nesnesini döndürür."""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def remove_book(self, isbn):
        """ISBN numarasına göre bir kitabı kütüphaneden siler ve dosyayı günceller."""
        book_to_remove = self.find_book(isbn)
        if book_to_remove:
            self.books.remove(book_to_remove)
            self.save_books()
            print(f"ISBN numaralı kitap '{isbn}' silindi.")
        else:
            print(f"Hata: '{isbn}' ISBN numaralı kitap bulunamadı.")

    def list_books(self):
        """Kütüphanedeki tüm kitapları listeler."""
        if not self.books:
            print("Kütüphanede hiç kitap yok.")
            return []
        print("\n--- Kütüphanedeki Kitaplar ---")
        for book in self.books:
            print(book)
        return self.books