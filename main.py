from book import Book
from library import Library

def main():
    library = Library()

    while True:
        print("\n--- Kütüphane Menüsü ---")
        print("1. Kitap Ekle (Sadece ISBN ile)")
        print("2. Kitap Sil")
        print("3. Kitapları Listele")
        print("4. Kitap Ara")
        print("5. Çıkış")

        choice = input("Seçiminizi yapın: ")

        if choice == "1":
            isbn = input("Eklenecek kitabın ISBN numarası: ")
            library.add_book(isbn)

        elif choice == "2":
            isbn = input("Silinecek kitabın ISBN numarası: ")
            library.remove_book(isbn)

        elif choice == "3":
            library.list_books()

        elif choice == "4":
            isbn = input("Aranacak kitabın ISBN numarası: ")
            book = library.find_book(isbn)
            if book:
                print(book)
            else:
                print("Kitap bulunamadı.")

        elif choice == "5":
            print("Çıkış yapılıyor...")
            break
        else:
            print("Geçersiz seçim!")

if __name__ == "__main__":
    main()