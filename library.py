import json
import os
from book import Book

class Library:
    class Library:
        def __init__(self, json_file="library.json"):
            self.json_file = json_file
            self.books = []
            if os.path.exists(self.json_file):
                with open(self.json_file, "r") as f:
                    data = json.load(f)
                    self.books = [Book(**book) for book in data]

    def load_books(self):
        with open(self.json_file, "r") as f:
            data = json.load(f)
            self.books = [Book(**b) for b in data]

    def save_books(self):
        with open(self.json_file, "w") as f:
            json.dump([b.__dict__ for b in self.books], f, indent=4)

    def add_book(self, book):
        self.books.append(book)
        self.save_books()

    def find_book(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def remove_book(self, isbn):
        self.books = [b for b in self.books if b.isbn != isbn]
        self.save_books()

    def list_books(self):
        return self.books
