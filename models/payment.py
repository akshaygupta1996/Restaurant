# from db import db
from models import db
import datetime
import random
from flask_restful_swagger import swagger

class PaymentModel(db.Model):

	__tablename__ = "payment"

	id = db.Column(db.Integer, primary_key = True)
	payment_type = db.Column(db.String(2), nullable = False)
	transaction_id = db.Column(db.String(12), unique = True, nullable = False)
	date_time_of_payment = db.Column(db.Date, datetime.datetime.now)
	amount = db.Column(db.Integer, nullable = False)
	# users = db.relationship('UsersModel', lazy = 'dynamic')

	def __init__(payment_type, transaction_id, date_time_of_payment, amount):
		self.payment_type = payment_type
		self.transaction_id = transaction_id
		self.date_time_of_payment= date_time_of_payment
		self.amount = amount


	def json(self):
		return {'id': self.id, 'payment_type': self.payment_type, 'transaction_id': self.transaction_id, 'date_time_of_payment': str(self.date_time_of_payment),'amount': self.amount}


	@classmethod
	def find_by_id(cls, id):
		return cls.query.filter_by(id = id).first()


	def save_to_db(self):
		db.session.add(self)
		db.session.commit()