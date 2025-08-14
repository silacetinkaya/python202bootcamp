from book import Book

def test_book_str():
    book = Book("Ulysses", "James Joyce", "978-0199535675")
    assert str(book) == "Ulysses by James Joyce (ISBN: 978-0199535675)"
