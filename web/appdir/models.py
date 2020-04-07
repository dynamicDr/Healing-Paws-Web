from datetime import datetime
from appdir import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, nullable=True)
    dob = db.Column(db.DateTime, index=True, nullable=True)
    address = db.Column(db.String(128), nullable=True)
    phone = db.Column(db.String(15), nullable=True)
    is_customer = db.Column(db.Boolean, index=True)
    questions = db.relationship('Question', backref='author', lazy='dynamic')
    answers = db.relationship('Answer', backref='author',lazy='dynamic')
    pets = db.relationship('Pet', backref='owner', lazy='dynamic')
    appointments = db.relationship('Appointment', backref='maker', lazy='dynamic')

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    booking_datetime = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.Date, index=True)
    time = db.Column(db.Integer)
    message = db.Column(db.String(32))
    status = db.Column(db.String(32))   #Pending/Confirmed/Canceled/Finished
    pet_status = db.Column(db.String(32))
    location = db.Column(db.String(32))
    is_emergency = db.Column(db.Boolean)
    accept_change = db.Column(db.Boolean)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    preferred_doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    assigned_doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
    
class Pet(db.Model):
    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    category = db.Column(db.String(32))
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    profession = db.Column(db.String(32))
    phone = db.Column(db.String(15), nullable=True)

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    anonymity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    
    
    def __repr__(self):
        return '<Question asked on {} by {}: {} >'.format(str(self.timestamp)[0:10],self.author.username,self.body)
        
class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))