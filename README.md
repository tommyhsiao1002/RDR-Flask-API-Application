# CRUD API Application for User Events Tracking

A local REST API service used in the library for booking and reserving study rooms and books using [Python Flask](http://flask.pocoo.org/) and [MySQL](https://www.mysql.com/) database.

## Description of the Architecture

For the database schema, we have serveral tables:

users

- user_id (Primary Key)
- username
- password

books

- book_id (Primary Key)
- title
- author
- publication_year

study_rooms

- study_room_id (Primary Key)
- location

book_reservations

- reservation_id (Primary Key)
- user_id (Foreign Key)
- book_id (Foreign Key)
- reservation_date

study_room_reservations

- reservation_id (Primary Key)
- user_id (Foreign Key)
- study_room_id (Foreign Key)
- reservation_date

I also assumed that the user was authenticated/logged in, so I seeded the users, book, and study_rooms tables with some sample data.

For the endpoint design,

1. The user can see/list all the events they have created with his/her user_id.

   Sending a 'GET' request to `http://127.0.0.1:5000/reservations/<user_id>`

2.

- The user can create a new book reservation by sending a 'POST' request to `http://127.0.0.1:5000/book_reservations`
- The user can create a new room reservation by sending a 'POST' request to `http://127.0.0.1:5000/room_reservations`

3.

- The user can pick a certain book reservation to view its data with a reservation_id.

  Sending a 'GET' request to `http://127.0.0.1:5000/book_reservations/<reservation_id>`

- The user can pick a certain room reservation to view its data with a reservation_id.

  Sending a 'GET' request to `http://127.0.0.1:5000/room_reservations/<reservation_id>`

4.

- The user can cancel a book reservation if needed with a reservation_id.

  Sending a 'DELETE' request to `http://127.0.0.1:5000/book_reservations/<reservation_id>`

- The user can cancel a room reservation if needed with a reservation_id.

  Sending a 'DELETE' request to `http://127.0.0.1:5000/room_reservations/<reservation_id>`

5.

- User can search a book reservation via the book_id.

  Sending a 'GET' request to `http://127.0.0.1:5000/book_reservations/book/<book_id>`

- User can search a study room reservation via the study_room_id.

  Sending a 'GET' request to `http://127.0.0.1:5000/room_reservations/room/<room_id>`

## Getting Started

### Prerequisites

Before running this project, make sure you have the following prerequisites:

- Python 3.9 or higher: [Download Python](https://www.python.org/downloads/)
- Pip package manager: [Installing Pip](https://pip.pypa.io/en/stable/installation/)
- MySQL (optional): [Installing MySQL](https://dev.mysql.com/downloads/)
  - I already set up a MySQL database on AWS RDS, so you may skip installing MySQL locally.
- curl (optional): [Installing curl](https://curl.se/download.html)
  - You can use Postman Instead [Postman Web](https://web.postman.co/home)

### Installation

1. Clone the repository

```shell
  git clone https://github.com/tommyhsiao1002/RDR-Flask-API-Application.git
  cd RDR-Flask-API-Application
```

2. Install the required dependencies

```shell
pip install -r requirements.txt
```


3. If you want to use your MySQL local database, make sure change this config line in app.py and seed_data.py

```python
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:admin1234@library-system.cmfgnyhl79y6.us-east-2.rds.amazonaws.com/library"
```

to

```python
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://username:password@localhost/db"
```

4. Create the tables and seed the data in the database

```shell
python3 seed_data.py
```
If using git bash
```shell
py seed_data.py
```

5. Start the Flask development server

```shell
python3 app.py
```
If using git bash
```shell
py app.py
```

### Sript Example

After running seed_data.py

- users table has a data "user_id=1, username='user1', password='12345678'"
- books table has ten example book data
- study_rooms table has six example study room data

We can test the endpoint by either Postman or curl:

**script a: The user can see/list all the events they have created with his/her user_id.**

1. Postman: Choose 'GET' request and type

```text
http://127.0.0.1:5000/reservations/1
```

2. curl:

```shell
curl http://127.0.0.1:5000/reservations/1
```

**script b:**

**- The user can create a new book reservation by sending a 'POST' request to `http://127.0.0.1:5000/book_reservations`**

1. Postman: Choose 'POST' request and add the data at body in JSON format

```text
http://127.0.0.1:5000/book_reservations
```

body

```
{"user_id": 1, "book_id": "9780261102217"}
```

2. curl:

```shell
curl -X POST -H "Content-Type: application/json" -d '{"user_id": 1, "book_id": "9780261102217"}' http://127.0.0.1:5000/book_reservations
```

**- The user can create a new study room reservation by sending a 'POST' request to `http://127.0.0.1:5000/room_reservations`**

1. Postman: Choose 'POST' request and add the data at body in JSON format

```text
http://127.0.0.1:5000/room_reservations
```

body

```
{"user_id": 1, "study_room_id": 1}
```

2. curl:

```shell
curl -X POST -H "Content-Type: application/json" -d '{"user_id": 1, "study_room_id": 1}' http://127.0.0.1:5000/room_reservations
```

**script c:**

**- The user can pick a certain book reservation to view its data with a reservation_id by sending a 'GET' request to `http://127.0.0.1:5000/book_reservations/<reservation_id>`**

1. Postman: Choose 'GET' request

```text
http://127.0.0.1:5000/book_reservations/1
```

2. curl:

```shell
curl http://127.0.0.1:5000/book_reservations/1
```

**- The user can pick a certain book reservation to view its data with a reservation_id by sending a 'GET' request to `http://127.0.0.1:5000/room_reservations/<reservation_id>`**

1. Postman: Choose 'GET' request

```text
http://127.0.0.1:5000/room_reservations/1
```

2. curl:

```shell
curl http://127.0.0.1:5000/room_reservations/1
```

**script d:**

**- The user can cancel a book reservation if needed with a reservation_id by sending a 'DELETE' request to `http://127.0.0.1:5000/book_reservations/<reservation_id>`**

1. Postman: Choose 'DELETE' request

```text
http://127.0.0.1:5000/book_reservations/1
```

2. curl:

```shell
curl -X "DELETE" http://127.0.0.1:5000/book_reservations/1
```

**- The user can cancel a book reservation if needed with a reservation_id by sending a 'DELETE' request to `http://127.0.0.1:5000/room_reservations/<reservation_id>`**

1. Postman: Choose 'DELETE' request

```text
http://127.0.0.1:5000/room_reservations/1
```

2. curl:

```shell
curl -X "DELETE" http://127.0.0.1:5000/room_reservations/1
```

**script d:**

**- The user can cancel a book reservation if needed with a reservation_id by sending a 'DELETE' request to `http://127.0.0.1:5000/room_reservations/room/<room_id>`>**

1. Postman: Choose 'DELETE' request

```text
http://127.0.0.1:5000/book_reservations/1
```

2. curl:

```shell
curl -X "DELETE" http://127.0.0.1:5000/book_reservations/1
```

**- The user can cancel a book reservation if needed with a reservation_id by sending a 'DELETE' request to `http://127.0.0.1:5000/room_reservations/<reservation_id>`**

1. Postman: Choose 'DELETE' request

```text
http://127.0.0.1:5000/room_reservations/1
```

2. curl:

```shell
curl -X "DELETE" http://127.0.0.1:5000/room_reservations/1
```

**script e:**

**- User can search a book reservation via the book_id by sending a 'GET' request to `http://127.0.0.1:5000/book_reservations/book/<book_id>`**

1. Postman: Choose 'GET' request

```text
http://127.0.0.1:5000/book_reservations/book/9780261102217
```

2. curl:

```shell
curl http://127.0.0.1:5000/book_reservations/book/9780261102217
```

**- User can search a room reservation via the book_id by sending a 'GET' request to `http://127.0.0.1:5000/room_reservations/room/<room_id>`**

1. Postman: Choose 'GET' request

```text
http://127.0.0.1:5000/room_reservations/room/1
```

2. curl:

```shell
curl http://127.0.0.1:5000/room_reservations/room/1
```
