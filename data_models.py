from flask_sqlalchemy import SQLAlchemy
#from app import app

db = SQLAlchemy()


class Author(db.Model):
    """Model representing an author in the library.

    Attributes:
        id (int): Unique identifier for the author.
        name (str): Name of the author.
        birth_date (date): Birth date of the author.
        date_of_death (date): Date of death of the author.
        books (list): List of books associated with the author.
    """
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    date_of_death = db.Column(db.Date, nullable=True)

    books = db.relationship('Book', backref='author_ref', lazy=True)

    def __repr__(self):
        return f'<Author {self.name}>'

    def __str__(self):
        return self.name


class Book(db.Model):
    """Model representing a book in the library.

        Attributes:
            id (int): Unique identifier for the book.
            isbn (str): ISBN number of the book.
            title (str): Title of the book.
            publication_year (int): Year the book was published.
            author_id (int): Foreign key referencing the author's ID.
            cover_image_url (str): URL for the book's cover image.
            author (Author): The author associated with the book.
        """
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    cover_image_url = db.Column(db.String(255))

    author = db.relationship('Author', backref='books_ref', lazy=True)

    def __repr__(self):
        return f'<Book {self.title} by {self.author_ref.name}>'

    def __str__(self):
        return f"{self.title} ({self.publication_year}) by {self.author_ref.name}"


#if __name__ == "__main__":
    #with app.app_context():
        #db.create_all()
