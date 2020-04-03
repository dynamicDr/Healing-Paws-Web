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