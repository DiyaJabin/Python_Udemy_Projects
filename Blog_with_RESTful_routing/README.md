\# Day 67 – Blog with RESTful Routing



Course project from a Udemy Python course.



This project is a blog website built using Flask that combines concepts learned in previous lessons such as RESTful routing, databases, forms, template rendering, and rich text editing.



\## Features

\- View all blog posts

\- Open individual blog pages

\- Create new blog posts

\- Edit existing posts

\- Delete blog posts

\- Store blog data using SQLite

\- Rich text editing using CKEditor

\- Flask-WTF forms with validation

\- Bootstrap-based responsive UI



\## Tech Used

\- Python

\- Flask

\- Flask-Bootstrap

\- Flask-WTF / WTForms

\- Flask-CKEditor

\- SQLite

\- SQLAlchemy

\- Jinja2

\- HTML/CSS



\## RESTful Routes Used

\- `GET /` → Show all posts

\- `GET /<post\_id>` → Show a specific post

\- `GET/POST /new-post` → Create a new post

\- `GET/POST /edit-post/<post\_id>` → Edit a post

\- `GET /delete-post/<post\_id>` → Delete a post



\## Run

1\. Install dependencies:

&#x20;  pip install flask flask-bootstrap flask-wtf flask-ckeditor flask-sqlalchemy



2\. Run the project:

&#x20;  python main.py



3\. Open in browser:

&#x20;  http://127.0.0.1:5003

