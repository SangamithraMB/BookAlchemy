# Book Alchemy

A simple library management system built with Flask and SQLAlchemy. This application allows users to manage authors and books, including adding new entries, searching for books, and displaying cover images using the Google Books API.

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Database Models](#database-models)
- [License](#license)

## Features

- Add and manage authors and books.
- Search for books by title or author name.
- View cover images for books using ISBN.
- Sort books by title or author.

## Technologies Used

- **Flask**: Web framework for building the application.
- **Flask-SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) for Flask.
- **Flask-Migrate**: Database migration tool for SQLAlchemy.
- **SQLite**: Lightweight database to store authors and books.
- **Jinja2**: Templating engine for rendering HTML.
- **Google Books API**: For fetching book cover images.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/library_management_system.git
   cd library_management_system
   ```
   
2. Install the required packages:
    ```bash
   pip install -r requirements.txt
   ```
   
## Usage

1.	Run the application:
   ```bash
    flask run
  ```

2.	Access the application:
Open your web browser and navigate to http://127.0.0.1:5000.

3. Adding Authors and Books:
	•	Navigate to the home page.
	•	Use the forms to add new authors and books.
4.	Searching for Books:
•	Use the search bar on the home page to find books by title or author.

## API Endpoints

	•	GET /: Home page, displays all authors and books.
	•	POST /add_author: Adds a new author to the database.
	•	POST /add_book: Adds a new book to the database.
	•	POST /search: Searches for books based on user input.
	•	POST /book/int:book_id/delete: Deletes a specified book from the database.

## Database Models

### Author

	•	id: Unique identifier for the author.
	•	name: Name of the author.
	•	birth_date: Birth date of the author (optional).
	•	date_of_death: Date of death of the author (optional).
	•	books: Relationship to the books associated with the author.

### Book

	•	id: Unique identifier for the book.
	•	isbn: ISBN number of the book.
	•	title: Title of the book.
	•	publication_year: Year the book was published.
	•	author_id: Foreign key referencing the author’s ID.
	•	cover_image_url: URL for the book’s cover image.
	•	author: Relationship to the author of the book.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

### Customization Tips

1. **Project Title**: Change the title if your project has a different name.
2. **Repository URL**: Update the GitHub URL to point to your actual repository.
3. **License**: If you have a specific license for your project, make sure to include that information.

Feel free to adjust any sections based on your project's specific details or your personal preferences! If you need further modifications or additions, just let me know.