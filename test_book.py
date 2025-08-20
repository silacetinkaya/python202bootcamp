from book import Book

def test_book_str():
    book = Book("Ulysses", "James Joyce", "978-0199535675")
    assert str(book) == "Ulysses by James Joyce (ISBN: 978-0199535675)"

def test_book_to_dict():
    book = Book("1984", "George Orwell", "9780451524935")
    expected = {
        "title": "1984",
        "author": "George Orwell",
        "isbn": "9780451524935"
    }
    assert book.to_dict() == expected
