class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"

    def to_dict(self):
        """Kitap bilgisini dict formatında döndürür (JSON kaydetmek için)."""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn
        }
