from flask_sqlalchemy import SQLAlchemy
#from app import app

db = SQLAlchemy()


class Author(db.Model):
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
