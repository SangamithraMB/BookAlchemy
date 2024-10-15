from flask import Flask, render_template, request, redirect, url_for, flash
from data_models import db, Author, Book
from flask_migrate import Migrate
from datetime import datetime
import os
import requests

app = Flask(__name__)

app.secret_key = os.urandom(24)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "data", "library.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
migrate = Migrate(app, db)

db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()


def get_cover_image(isbn):
    """Fetch the cover image URL for a book using its ISBN.

        Args:
            isbn (str): The ISBN of the book.

        Returns:
            str: The URL of the book's cover image if found, otherwise None.
    """
    url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if "items" in data:
            cover_image_url = data["items"][0]["volumeInfo"].get("imageLinks", {}).get("thumbnail")
            return cover_image_url
    return None


@app.route('/')
def home():
    """Render the home page, displaying a list of books and authors.

    The list can be sorted by title or author based on user input.
    """
    sort_by = request.args.get('sort')
    if sort_by == 'title':
        books = Book.query.order_by(Book.title).all()  # Sort by title
    elif sort_by == 'author':
        books = Book.query.join(Author).order_by(Author.name).all()  # Sort by author
    else:
        books = Book.query.all()

    authors = Author.query.all()
    print(f'Authors: {authors}')
    print(f'Books: {books}')
    return render_template('home_chatgpt.html', authors=authors, books=books)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Handle the addition of a new author.

    GET: Render the form for adding a new author.
    POST: Process the submitted form to add the author to the database.
    """
    if request.method == 'POST':
        name = request.form['name']
        birthdate_string = request.form['birthdate']
        date_of_death_string = request.form.get('date_of_death', None)
        birthdate_object = datetime.strptime(birthdate_string, "%Y-%m-%d").date()

        date_of_death_object = None
        if date_of_death_string:
            date_of_death_object = datetime.strptime(date_of_death_string, "%Y-%m-%d").date()

        try:
            if name:
                new_author = Author(name=name, birth_date=birthdate_object, date_of_death=date_of_death_object)
                db.session.add(new_author)
                db.session.commit()
                flash('Author added successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Name is required!', 'danger')

        except Exception as e:
            error_message = str(e)
            return render_template('add_author.html', error_message=error_message)

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Handle the addition of a new book.

    GET: Render the form for adding a new book.
    POST: Process the submitted form to add the book to the database.
    """
    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']
        cover_image_url = get_cover_image(isbn)

        try:
            if isbn and title and publication_year:
                new_book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id,
                                cover_image_url=cover_image_url)
                db.session.add(new_book)
                db.session.commit()
                flash('Book added successfully!', 'success')
                return redirect(url_for('home'))
            else:
                flash('All fields are required!', 'danger')

        except Exception as e:
            error_message = str(e)
            return render_template('add_book.html', error_message=error_message)
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/search', methods=['POST'])
def search():
    """Search for books based on a query string.

    The search checks both book titles and author names for matches.
    """
    query = request.form['query']
    if query:
        books = Book.query.filter(
            (Book.title.ilike(f'%{query}%')) |
            (Author.name.ilike(f'%{query}%'))
        ).join(Author).all()
    else:
        books = []

    return render_template('home_chatgpt.html', books=books)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """Delete a specific book by its ID.

    If the author has no other books left, the author is also deleted.
    """
    book = Book.query.get_or_404(book_id)
    author_id = book.author_id  # Store the author_id before deleting the book

    try:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')

        # Check if the author has any other books
        author = Author.query.get(author_id)
        if author and not author.books:  # Check if the author has no books left
            db.session.delete(author)
            db.session.commit()
            flash('Author deleted successfully as they have no books left!', 'success')

    except Exception:
        db.session.rollback()
        flash('An error occurred while deleting the book. Please try again.', 'danger')

    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
