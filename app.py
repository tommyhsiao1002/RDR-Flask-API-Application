from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://user:password@localhost/db"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://admin:admin1234@library-system.cmfgnyhl79y6.us-east-2.rds.amazonaws.com/test"


app.config['SECRET_KEY'] = 'thisisasecretkey'
db = SQLAlchemy(app)


class Users(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
        }


class Books(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.String(
        13, collation='utf8mb4_0900_ai_ci'), primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer)

    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'publication_year': str(self.publication_year)
        }


class StudyRooms(db.Model):
    __tablename__ = 'study_rooms'
    study_room_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'study_room_id': self.study_room_id,
            'location': self.location,
        }


class BookReservations(db.Model):
    __tablename__ = 'book_reservations'
    reservation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    book_id = db.Column(db.String(
        13, collation='utf8mb4_0900_ai_ci'), db.ForeignKey(
        'books.book_id'), nullable=False)
    reservation_date = db.Column(db.Date)

    def to_dict(self):
        return {
            'reservation_id': self.reservation_id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'reservation_date': str(self.reservation_date)
        }


class StudyRoomReservations(db.Model):
    __tablename__ = 'study_room_reservations'
    reservation_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)
    study_room_id = db.Column(db.Integer, db.ForeignKey(
        'study_rooms.study_room_id'), nullable=False)
    reservation_date = db.Column(db.Date)

    def to_dict(self):
        return {
            'reservation_id': self.reservation_id,
            'user_id': self.user_id,
            'study_room_id': self.study_room_id,
            'reservation_date': str(self.reservation_date)
        }


# endpoint for solution a.
# to retrieve all events created by a user
@app.route('/reservations/<user_id>', methods=['GET'])
def show_all_reservations(user_id):
    # get all book reservations by user_id
    book_reservations = BookReservations.query.filter_by(user_id=user_id).all()
    # get all study room reservations by user_id
    room_reservations = StudyRoomReservations.query.filter_by(
        user_id=user_id).all()
    # convert BookReservations to dict
    book_list = [book_reservation.to_dict()
                 for book_reservation in book_reservations]
    # convert StudyRoomReservations to dict type
    room_list = [room_reservation.to_dict()
                 for room_reservation in room_reservations]
    # return the result in json format
    return jsonify(book_list + room_list)


# endpoint for solution b.
# create a new book reservation
@app.route('/book_reservations', methods=['POST'])
def create_book_reservation():
    # access the posted data
    data = request.get_json()
    if not data:
        return jsonify({'Error': "No data provided"})
    # handle the error of user not existed
    all_users = Users.query.all()
    all_users = [user.to_dict() for user in all_users]
    all_users_id_list = [user["user_id"]for user in all_users]
    if data.get('user_id') not in all_users_id_list:
        return jsonify({'message': 'No user existed'})

    # handle the error of book not existed
    all_books = Books.query.all()
    all_books = [book.to_dict() for book in all_books]
    all_books_id_list = [book["book_id"]for book in all_books]
    if data.get('book_id') not in all_books_id_list:
        return jsonify({'message': 'No book existed'})

    # extract relevent fields from the data
    new_reservation = BookReservations(reservation_id=data.get('reservation_id'), user_id=data.get('user_id'),
                                       book_id=data.get('book_id'), reservation_date=datetime.now())
    # Add the event to the session and commit to the database
    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({'message': 'Data received and processed successfully'})


# create a new room reservation
@app.route('/room_reservations', methods=['POST'])
def create_room_reservation():
    # access the posted data
    data = request.get_json()
    if not data:
        return jsonify({'Error': "No data provided"})
    # handle the error of user not existed
    all_users = Users.query.all()
    all_users = [user.to_dict() for user in all_users]
    all_users_id_list = [user["user_id"]for user in all_users]
    if data.get('user_id') not in all_users_id_list:
        return jsonify({'message': 'No user existed'})

    # handle the error of book not existed
    all_rooms = StudyRooms.query.all()
    all_rooms = [room.to_dict() for room in all_rooms]
    all_rooms_id_list = [room["study_room_id"]for room in all_rooms]
    if data.get('study_room_id') not in all_rooms_id_list:
        return jsonify({'message': 'No room existed'})
    # extract relevent fields from the data
    new_reservation = StudyRoomReservations(reservation_id=data.get('reservation_id'), user_id=data.get('user_id'),
                                            study_room_id=data.get('study_room_id'), reservation_date=datetime.now())
    # Add the event to the session and commit to the database
    db.session.add(new_reservation)
    db.session.commit()

    return jsonify({'message': 'Data received and processed successfully'})


# endpoint for solution c.
# view a book reseravation
@app.route('/book_reservations/<reservation_id>', methods=['GET'])
def view_book_reservation(reservation_id):
    # handle the error of a reservation not existed
    all_reservation_data = BookReservations.query.all()
    all_reservations = [reservation.to_dict()
                        for reservation in all_reservation_data]
    all_reservation_id_list = [reservation["reservation_id"]
                               for reservation in all_reservations]
    if int(reservation_id) not in all_reservation_id_list:
        return jsonify({'message': 'No reservation existed'})

    reservation = BookReservations.query.filter_by(
        reservation_id=reservation_id).one()
    reservation_data = reservation.to_dict()
    book_id = reservation_data['book_id']
    book_data = Books.query.filter_by(book_id=book_id).one()
    del reservation_data['book_id']
    reservation_data.update(book_data.to_dict())
    return jsonify(reservation_data)


# view a room reseravation
@app.route('/room_reservations/<reservation_id>', methods=['GET'])
def view_room_reservation(reservation_id):
    # handle the error of a reservation not existed
    all_reservation_data = StudyRoomReservations.query.all()
    all_reservations = [reservation.to_dict()
                        for reservation in all_reservation_data]
    all_reservation_id_list = [reservation["reservation_id"]
                               for reservation in all_reservations]
    if int(reservation_id) not in all_reservation_id_list:
        return jsonify({'message': 'No reservation existed'})

    reservation = StudyRoomReservations.query.filter_by(
        reservation_id=reservation_id).one()
    reservation_data = reservation.to_dict()
    study_room_id = reservation_data['study_room_id']
    room_data = StudyRooms.query.filter_by(study_room_id=study_room_id).one()
    del reservation_data['study_room_id']
    reservation_data.update(room_data.to_dict())
    return jsonify(reservation_data)


# endpoint for solution d.
# delete an book reservation
@app.route('/book_reservations/<reservation_id>', methods=['DELETE'])
def delete_book_reservation(reservation_id):
    # handle the error of a reservation not existed
    all_reservation_data = BookReservations.query.all()
    all_reservations = [reservation.to_dict()
                        for reservation in all_reservation_data]
    all_reservation_id_list = [reservation["reservation_id"]
                               for reservation in all_reservations]
    if int(reservation_id) not in all_reservation_id_list:
        return jsonify({'message': 'No reservation existed'})

    # Find the data to be deleted in the database
    data = BookReservations.query.get(reservation_id)

    # Check if the data exists
    if not data:
        return jsonify({'error': 'Data not found'})

    # Delete the data from the database
    db.session.delete(data)
    db.session.commit()

    # Return a response indicating successful deletion
    return jsonify({'message': 'Data deleted successfully'})


# delete an room reservation
@app.route('/room_reservations/<reservation_id>', methods=['DELETE'])
def delete_room_reservation(reservation_id):
    # handle the error of a reservation not existed
    all_reservation_data = StudyRoomReservations.query.all()
    all_reservations = [reservation.to_dict()
                        for reservation in all_reservation_data]
    all_reservation_id_list = [reservation["reservation_id"]
                               for reservation in all_reservations]
    if int(reservation_id) not in all_reservation_id_list:
        return jsonify({'message': 'No reservation existed'})
    # Find the data to be deleted in the database
    data = StudyRoomReservations.query.get(reservation_id)

    # Check if the data exists
    if not data:
        return jsonify({'error': 'Data not found'})

    # Delete the data from the database
    db.session.delete(data)
    db.session.commit()

    # Return a response indicating successful deletion
    return jsonify({'message': 'Data deleted successfully'})


#  search the book reservations via book_id
@app.route('/book_reservations/book/<book_id>', methods=['GET'])
def search_book_reservation(book_id):
    book_reservations = BookReservations.query.filter_by(
        book_id=book_id).all()
    book_list = [book_reservation.to_dict()
                 for book_reservation in book_reservations]
    return jsonify(book_list)


#  search the room reservations via book_id
@app.route('/room_reservations/room/<room_id>', methods=['GET'])
def search_room_reservation(room_id):
    room_reservations = StudyRoomReservations.query.filter_by(
        study_room_id=room_id).all()
    room_list = [room_reservation.to_dict()
                 for room_reservation in room_reservations]
    return jsonify(room_list)

print(__name__)
if __name__ == "__main__":
    app.run(debug=True)
