import pytest
from library import Library
from book import Book

def test_add_and_find_book(tmp_path):
    json_file = tmp_path / "library.json"
    lib = Library(str(json_file))

    book = Book("1984", "George Orwell", "9780451524935")
    lib.add_book(book)

    found = lib.find_book("9780451524935")
    assert found is not None
    assert found.title == "1984"
    assert found.author == "George Orwell"

def test_remove_book(tmp_path):
    json_file = tmp_path / "library.json"
    lib = Library(str(json_file))

    book = Book("1984", "George Orwell", "9780451524935")
    lib.add_book(book)

    removed = lib.remove_book("9780451524935")
    assert removed is True
    assert lib.find_book("9780451524935") is None

def test_list_books(tmp_path):
    json_file = tmp_path / "library.json"
    lib = Library(str(json_file))

    book1 = Book("1984", "George Orwell", "9780451524935")
    book2 = Book("Ulysses", "James Joyce", "9780199535675")
    lib.add_book(book1)
    lib.add_book(book2)

    books = lib.list_books()
    assert len(books) == 2
    titles = [b.title for b in books]
    assert "1984" in titles
    assert "Ulysses" in titles
