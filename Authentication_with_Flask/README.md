\# Day 68 – Flask Authentication Website



Course project from a Udemy Python course.



This project is a basic authentication website built with Flask.  

It focuses on user registration, login, logout, protected routes, password hashing, salting, and flash messages.



\## Features

\- User registration

\- User login and logout

\- Password hashing and salting using Werkzeug

\- User session management with Flask-Login

\- Protected routes using `login\_required`

\- Flash messages for login/register feedback

\- Download page accessible only to logged-in users

\- User data stored in SQLite using SQLAlchemy

\- Template inheritance with Jinja



\## Tech Used

\- Python

\- Flask

\- Flask-Login

\- Flask-SQLAlchemy

\- SQLite

\- Werkzeug Security

\- Jinja2

\- HTML/CSS

\- Bootstrap



\## Run

1\. Install dependencies:

&#x20;  pip install flask flask-sqlalchemy flask-login python-dotenv



2\. Create a `.env` file:

&#x20;  SECRET\_KEY=your\_secret\_key\_here



3\. Run the app:

&#x20;  python main.py



4\. Open in browser:

&#x20;  http://127.0.0.1:5000

