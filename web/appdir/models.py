from datetime import datetime
from appdir import db


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True)
    dob = db.Column(db.DateTime, index=True)
    password_hash = db.Column(db.String(128))
    address = db.Column(db.String(128))
    phone = db.Column(db.String(15))
   
    # posts = relationship('Post', backref='author', lazy='dynamic')
    # topic = relationship('Topic', backref='maker', lazy='dynamic')

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(20))
    questions = db.relationship('Question', backref='author', lazy='dynamic')
    answers = db.relationship('Answer', backref='author',lazy='dynamic')
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    anonymity = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    answers = db.relationship('Answer', backref='question', lazy='dynamic')
    
    
    def __repr__(self):
        return '<Question asked on {} by {}: {} >'.format(str(self.timestamp)[0:10],self.author.username,self.body)
        
class Answer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.String(140))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))