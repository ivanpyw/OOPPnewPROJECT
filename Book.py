import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("../secret/firebase.json")

firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://librarysystem-93143.firebaseio.com/'
})

root = db.reference('books')

class Book:

    def __init__(self, isbn_no, title, author_name, genre, publisher, published_date, synopsis, price, status,
                 created_by, create_date):
        self.isbn_no = isbn_no
        self.title = title
        self.author_name = author_name
        self.genre = genre
        self.publisher = publisher
        self.published_date = published_date
        self.synopsis = synopsis
        self.price = price
        self.status = status
        self.created_by = created_by
        self.create_date = create_date

    def retrieve_book_by_isbn(self,isbn):
        pass

    def save_book(self, aBook):
        pass

    def delete_book(self, isbn):
        pass

    def update_book(self, aBook):
        pass

    def retrieve_all_books(self):
        pass

