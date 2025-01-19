from functools import reduce

# Books class
class Book:
    def __init__(self, id=0, title="undefined", price=0.0, available = False):
        self.__id = id
        self.__title = title
        self.__price = price
        self.__available = available

    # Getter and Setters
    # id
    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if value < 0:
            raise ValueError("ID cannot be negative.")
        self.__id = value

    # title
    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        self.__title = value

    # price
    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value):
        if value < 0:
            raise ValueError("Price cannot be negative.")
        self.__price = value

    # available
    @property
    def available(self):
        return self.__available

    @available.setter
    def available(self, value):
        if isinstance(value, bool):
            self.__available = value
        elif value.strip().lower() in ["yes", "no"]:
            self.__available = value.strip().lower() == "yes"
        else:
            raise ValueError("Available must be 'yes' or 'no'.")

    # For displaying
    def __str__(self):
        return f"ID: {self.__id}, Title: {self.__title}, Price: {self.__price:.2f}$, Available: {"Yes" if self.__available else "No"}"

    def toggle_availability(self):
        self.__available = not self.__available

# Library class
class Library:
    books = []

    # My constructor
    def __init__(self, books):
        self.books = [Book(book['id'], book['title'], book['price'], book['available']) for book in books]

    # for adding books
    def add_book(self):
        print("\nEnter book details:")

        try:
            book = Book()

            id = int(input("ID: "))
            book.id = id

            is_exist = any(book.id == id for book in self.books)

            # check if other book with this ID exists
            if is_exist:
                print("\nBook with this ID already exists.")
                return

            title = str(input("Title: ")).strip()
            book.title = title

            price = float(input("Price: "))
            book.price = price

            available = input("Available (yes/no): ").strip().lower()
            book.available = available

            self.books.append(book)
            print(f'\nBook "{book.title}" added successfully!')

        except Exception as e:
            print(f"\nError: {e}")

    # borrowing the book
    def borrow_book(self):
        try:
            id = int(input("\nEnter book ID to borrow: "))

            for book in self.books:
                if book.id == id:
                    if not book.available:
                        print("\nBook is already borrowed.")
                        return

                    book.toggle_availability()
                    print(f'\nBook "{book.title}" borrowed successfully!')
                    return

            print("Book not found.")
        except Exception as e:
            print(f"\nError: {e}")

    # for returning, the same logic as the borrowing book
    def return_book(self):
        id = int(input("\nEnter book ID to return: "))
        try:
            for book in self.books:
                if book.id == id:
                    if book.available:
                        print("\nBook is already returned!")
                        return

                    book.toggle_availability()
                    print(f'\nBook "{book.title}" returned successfully!')
                    return

            print("Book not found.")
        except Exception as e:
            print(f"\nError: {e}")

    # displaying array of books
    def display_books(self):
        print("\nBooks in the library:")

        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book.__str__()}")

# Child class EBook extends parent class Book
class EBook(Book):
    # super is excellently looks, making code more readable
    def __init__(self, id=0, title="undefined", price=0.0, available=False, file_size=0.0):
        super().__init__(id, title, price, available)
        self.__file_size = file_size

    # simple getter and setter for file_size
    @property
    def file_size(self):
        return self.__file_size

    @file_size.setter
    def file_size(self, value):
        if value < 0:
            raise ValueError("File size cannot be negative.")
        self.__file_size = value

    # Here I am using overriding
    def __str__(self):
        return f"{super().__str__()}, File Size: {self.__file_size} MB"

# sorting by price function
def sort_books_by_price(library):
    sort_type = input("Sort books by price (ascending/descending): ").strip().lower()
    if sort_type == "ascending" or sort_type == "descending":
        library.books.sort(key=lambda book: book.price, reverse=(sort_type == "ascending"))

    print("Books sorted by price: ")
    library.display_books()

# finding by user typed keyword
def find_books_by_title(library):
    keyword = input("Enter keyword to search for: ").strip().lower()

    found_books = list(filter(lambda book: keyword in book.title.lower(), library.books))

    if found_books:
        print("\nBooks matching your search:")
        for i, book in enumerate(found_books, 1):
            print(f"{i}. {book.__str__()}")

    # handling the case when no books
    else:
        print("No books found with the given keyword.")

# display for terminal program
def display_menu():
    print("\n--- Library Management System ---")
    print("1. Add a book")
    print("2. Display all books")
    print("3. Borrow a book")
    print("4. Return a book")
    print("5. Search for books by title")
    print("6. Sort books by price")
    print("7. Exit")


def main():
    # list of dictionary
    books_data = [
        {"id": 1, "title": "Python Programming", "price": 29.99, "available": True},
        {"id": 2, "title": "Advanced Python", "price": 39.99, "available": False},
        {"id": 3, "title": "Learn Java", "price": 25.49, "available": True},
        {"id": 4, "title": "Data Science with Python", "price": 45.99, "available": True},
        {"id": 5, "title": "Python for Data Science", "price": 19.99, "available": False}
    ]

    # storing the available books with filter
    available_books = list(filter(lambda book: book['available'], books_data))

    # total value of books
    total_value = reduce(lambda acc, book: acc + book['price'], books_data, 0)

    # giving the type of library to books_data
    library = Library(books_data)
    try:
        while True:
            display_menu()
            choice = input("\n\nYour choice: ").strip()

            if choice == "1":
                library.add_book()
            elif choice == "2":
                library.display_books()
                print(f"\nTotal value of all books: {total_value:.2f}$")
            elif choice == "3":
                library.borrow_book()
            elif choice == "4":
                library.return_book()
            elif choice == "5":
                find_books_by_title(library)
            elif choice == "6":
                sort_books_by_price(library)
            elif choice == "7":
                print("Thank you for using the Mini Library System!")
                break
            else:
                print("Invalid option. Please try again.")

    # i want to handle the case when user manually stopped program
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting gracefully.")

if __name__ == "__main__":
    main()
