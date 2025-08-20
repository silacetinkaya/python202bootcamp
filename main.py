from library import Library, fetch_book_from_api


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
            isbn = input("Eklenecek kitabın ISBN numarası: ").strip()
            if not isbn:
                print("ISBN boş olamaz!")
                continue

            book = fetch_book_from_api(isbn)
            if book:
                library.add_book(book)

        elif choice == "2":
            isbn = input("Silinecek kitabın ISBN numarası: ").strip()
            if library.remove_book(isbn):
                print("Kitap başarıyla silindi.")

        elif choice == "3":
            books = library.list_books()
            if not books:
                print("Kütüphanede hiç kitap yok.")
            else:
                print("\n--- Kütüphanedeki Kitaplar ---")
                for book in books:
                    print(book)

        elif choice == "4":
            isbn = input("Aranacak kitabın ISBN numarası: ").strip()
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
