import os
import json
from library import Library, Book

def test_add_and_find_book(tmp_path):
    # Test için geçici json dosyası oluştur
    json_file = tmp_path / "library.json"
    lib = Library(str(json_file))

    # Kitap ekle
    book = Book("1984", "George Orwell", "9780451524935")
    lib.add_book(book)

    # Kitap var mı?
    found = lib.find_book("9780451524935")
    assert found is not None
    assert found.title == "1984"
    assert found.author == "George Orwell"

def test_remove_book(tmp_path):
    json_file = tmp_path / "library.json"
    lib = Library(str(json_file))
    book = Book("1984", "George Orwell", "9780451524935")
    lib.add_book(book)

    lib.remove_book("9780451524935")
    assert lib.find_book("9780451524935") is None

def test_list_books(tmp_path):
    json_file = tmp_path / "library.json"
    lib = Library(str(json_file))
    lib.add_book(Book("1984", "George Orwell", "9780451524935"))
    books = lib.list_books()
    assert len(books) == 1
    assert books[0].title == "1984"
