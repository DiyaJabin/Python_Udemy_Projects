\# Day 66 – RESTful Cafe API



Course project from a Udemy Python course.



This project is a RESTful API built using Flask, SQLite, and SQLAlchemy.  

The API allows users to retrieve, add, update, and delete cafe data while testing endpoints using Postman.



\## Features

\- Get a random cafe

\- Retrieve all cafes

\- Search cafes by location

\- Add a new cafe

\- Update cafe coffee prices

\- Delete cafes using an API key

\- JSON responses using Flask jsonify()



\## Tech Used

\- Python

\- Flask

\- SQLite

\- SQLAlchemy

\- REST APIs

\- Postman



\## API Endpoints



\### GET

\- `/random` → Get a random cafe

\- `/all` → Get all cafes

\- `/search?loc=LOCATION` → Search cafes by location



\### POST

\- `/add` → Add a new cafe



\### PATCH

\- `/update-price/<cafe\_id>?new\_price=VALUE` → Update coffee price



\### DELETE

\- `/report-closed/<cafe\_id>?api\_key=TopSecretAPIKey` → Delete a cafe



\## Run

1\. Install dependencies:

&#x20;  pip install flask flask-sqlalchemy



2\. Run the app:

&#x20;  python main.py



3\. Open:

&#x20;  http://127.0.0.1:5000

