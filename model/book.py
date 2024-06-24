from service.db import db

class Book(db.Model):
    db.__tablename__ = 'books'
    bookId = db.Column(db.String(100), primary_key=True, autoincrement=False)
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, default=0)
    description = db.Column(db.Text, default='')
    isbn = db.Column(db.String(13), nullable=False)
    numRatings = db.Column(db.Integer, default=0)
    coverImg = db.Column(db.String(100), default='')
    pages = db.Column(db.Integer, default=0)
    genres = db.relationship('Genre', secondary='book_genres', lazy='subquery', backref=db.backref('books', lazy=True))
    authors = db.relationship('Author', secondary='author_books', lazy='subquery', backref=db.backref('books', lazy=True))
    
book_genres = db.Table('book_genres',
                       db.Column('bookId', db.String(100), db.ForeignKey('books.bookId'), primary_key=True),
                       db.Column('genreId', db.Integer, db.ForeignKey('genres.genreId'), primary_key=True))

author_books = db.Table('author_books',
                        db.Column('authorId', db.Integer, db.ForeignKey('authors.authorId'), primary_key=True),
                        db.Column('bookId', db.String(100), db.ForeignKey('books.bookId'), primary_key=True))