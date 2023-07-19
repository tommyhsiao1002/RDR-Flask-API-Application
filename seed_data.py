from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user:password@localhost/db"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:admin1234@library-system.cmfgnyhl79y6.us-east-2.rds.amazonaws.com/test"
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.String(
        13, collation='utf8mb4_0900_ai_ci'), primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer)


class StudyRooms(db.Model):
    __tablename__ = 'study_rooms'
    study_room_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)


class BookReservations(db.Model):
    __tablename__ = 'book_reservations'
    reservation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    book_id = db.Column(db.String(
        13, collation='utf8mb4_0900_ai_ci'), db.ForeignKey(
        'books.book_id'), nullable=False)
    reservation_date = db.Column(db.Date)


class StudyRoomReservations(db.Model):
    __tablename__ = 'study_room_reservations'
    reservation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    study_room_id = db.Column(db.Integer, db.ForeignKey(
        'study_rooms.study_room_id'), nullable=False)
    reservation_date = db.Column(db.Date)


# Create a function to add an authenticated/logged-in user into the 'users' table
def seed_users():
    user1 = Users(user_id=1, username='user1', password='12345678')
    db.session.add(user1)
    db.session.commit()


# Create a function to seed 10 books data into the 'books' table
def seed_books():
    books_data = [
        {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'publication_year': 1925,
            'isbn': '9780743273565'
        },
        {
            'title': 'To Kill a Mockingbird',
            'author': 'Harper Lee',
            'publication_year': 1960,
            'isbn': '9780061120084'
        },
        {
            'title': '1984',
            'author': 'George Orwell',
            'publication_year': 1949,
            'isbn': '9780451524935'
        },
        {
            'title': 'Pride and Prejudice',
            'author': 'Jane Austen',
            'publication_year': 1813,
            'isbn': '9780141439518'
        },
        {
            'title': 'The Catcher in the Rye',
            'author': 'J.D. Salinger',
            'publication_year': 1951,
            'isbn': '9780316769174'
        },
        {
            'title': 'Harry Potter and the Philosopher\'s Stone',
            'author': 'J.K. Rowling',
            'publication_year': 1997,
            'isbn': '9780590353427'
        },
        {
            'title': 'The Hobbit',
            'author': 'J.R.R. Tolkien',
            'publication_year': 1937,
            'isbn': '9780261102217'
        },
        {
            'title': 'To the Lighthouse',
            'author': 'Virginia Woolf',
            'publication_year': 1927,
            'isbn': '9780156907392'
        },
        {
            'title': 'Moby-Dick',
            'author': 'Herman Melville',
            'publication_year': 1851,
            'isbn': '9781853260087'
        },
        {
            'title': 'The Lord of the Rings',
            'author': 'J.R.R. Tolkien',
            'publication_year': 1954,
            'isbn': '9780261102354'
        }
    ]
    for book in books_data:
        new_book = Books(title=book['title'], author=book['author'],
                         publication_year=book['publication_year'], book_id=book['isbn'])
        db.session.add(new_book)

    db.session.commit()


# Create a function to seed study room data into the 'studyrooms' table
def seed_studyrooms():
    studyroom_data = [
        {
            'id': 1,
            'location': 'Library'
        },
        {
            'id': 2,
            'location': 'Quiet Study Area'
        },
        {
            'id': 3,
            'location': 'Student Center'
        },
        {
            'id': 4,
            'location': 'Computer Lab'
        },
        {
            'id': 5,
            'location': 'Science Building'
        },
        {
            'id': 6,
            'location': 'Art Studio'
        }
    ]

    for studyroom in studyroom_data:
        new_studyroom = StudyRooms(
            study_room_id=studyroom['id'], location=studyroom['location'])
        db.session.add(new_studyroom)

    db.session.commit()


if __name__ == '__main__':
    # Initialize the database and seed the data
    with app.app_context():
        db.create_all()
        seed_users()
        seed_books()
        seed_studyrooms()
