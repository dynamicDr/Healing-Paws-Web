from datetime import datetime
from appdir import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_customer = db.Column(db.Boolean, index=True)
    ref_id = db.Column(db.Integer)
    questions = db.relationship('Question', backref='author', lazy='dynamic')
    answers = db.relationship('Answer', backref='author',lazy='dynamic')
    pets = db.relationship('Pet', backref='owner', lazy='dynamic')
    # appointments = db.relationship('Appointment', backref='maker', lazy='dynamic') #Appointment表里有两个User的外键，所以这里不能反向查询

class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    dob = db.Column(db.Date)
    email = db.Column(db.String(32), index=True, nullable=True)
    address = db.Column(db.String(64), nullable=True)
    phone = db.Column(db.String(15), nullable=True)

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    loc = db.Column(db.Integer, nullable=False)
    intro = db.Column(db.String(32), nullable=True)

class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.now)# 提交的时间
    description = db.Column(db.String(32), default='')
    status = db.Column(db.String(32), default='Pending')   #Pending/Confirmed/Canceled/Finished
    pet_status = db.Column(db.String(32), default='Unchecked')  #设计一系列状态
    loc = db.Column(db.Integer)
    is_emergency = db.Column(db.Boolean)
    changeable = db.Column(db.Boolean)
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    pet_id = db.Column(db.Integer, db.ForeignKey('pets.id'))
    preferred_doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
class Pet(db.Model):
    __tablename__ = 'pets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))
    age = db.Column(db.Integer)
    category = db.Column(db.String(32))# dog/cat
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    anonymity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    counta = db.Column(db.Integer,default=0)
    
    def __repr__(self):
        return '<Question asked on {} by {}: {} >'.format(str(self.timestamp)[0:10],self.author.username,self.body)
        
class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
