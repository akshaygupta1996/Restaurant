from db import db
import datetime
import random
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
	refcode = db.Column(db.String(8), unique = True)
	register_ref = db.Column(db.String(8), default = "00000000")
	register_ref_no = db.Column(db.Integer, default=0)
	created_at = db.Column(db.Date, default=datetime.datetime.now)
	updated_at = db.Column(db.Date, onupdate=datetime.datetime.now)
	address = db.relationship('UsersAddressModel', lazy = 'dynamic')
	promo = db.relationship('UserPromoModel', lazy = 'dynamic')
	

	def __init__(self,fname,lname,email,phone_number,password, refcode, register_ref, register_ref_no):
		self.fname = fname
		self.lname = lname
		self.email = email
		self.phone_number = phone_number
		self.password = password
		self.refcode = refcode
		self.register_ref = register_ref
		self.register_ref_no = register_ref_no

	def json(self):
		return { 'id': self.id, 'fname': self.fname, 'lname': self.lname, 'email': self.email, 'phone_number': self.phone_number, 'refcode': self.refcode}

	@classmethod
	def find_by_email(cls, email):

		return cls.query.filter_by(email = email).first()

	@classmethod
	def find_by_phone(cls, phone_number):

		return cls.query.filter_by(phone_number = phone_number).first()

	@classmethod
	def find_by_refcode(cls, refcode):
		return cls.query.filter_by(refcode = refcode).first()

	@classmethod
	def getRefCode(cls, fname):
		ref = str(random.randint(1000, 9999))
		ref = fname[:4] + ref

		user_ref = UsersModel.find_by_refcode(ref)
		if user_ref is None:
			return ref
		else:
			getRefCode(fname)

	def save_to_db(self):

		db.session.add(self)
		db.session.commit()

