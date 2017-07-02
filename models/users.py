from db import db
import datetime
from flask_restful_swagger import swagger

@swagger.model
class UsersModel(db.Model):

	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key = True)
	fname = db.Column(db.String(20))
	lname = db.Column(db.String(20))
	email = db.Column(db.String(80), unique = True)
	phone_number = db.Column(db.String(10), unique = True)
	password = db.Column(db.String(15), nullable = False)
	created_at = db.Column(db.Date, default=datetime.datetime.now)
	updated_at = db.Column(db.Date, onupdate=datetime.datetime.now)
	address = db.relationship('UsersAddressModel', lazy = 'dynamic')

	def __init__(self,fname,lname,email,phone_number,password):
		self.fname = fname
		self.lname = lname
		self.email = email
		self.phone_number = phone_number
		self.password = password

	def json(self):
		return { 'id': self.id, 'fname': self.fname, 'lname': self.lname, 'email': self.email, 'phone_number': self.phone_number}

	@classmethod
	def find_by_email(cls, email):

		return cls.query.filter_by(email = email).first()

	@classmethod
	def find_by_phone(cls, phone_number):

		return cls.query.filter_by(phone_number = phone_number).first()

	def save_to_db(self):

		db.session.add(self)
		db.session.commit()

