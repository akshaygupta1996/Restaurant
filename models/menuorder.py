from db import db
import datetime
import random
from flask_restful_swagger import swagger

@swagger.model
class MenuOrderModel(db.Model):

	__tablename__ = "menuorder"

	id = db.Column(db.Integer, primary_key = True)
	order_id = db.Column(db.String(10), unique = True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
	address_id = db.Column(db.Integer, db.ForeignKey('users_address.id'))
	promo_code = db.Column(db.String(10), nullable = True)
	special_note = db.Column(db.String(100), nullable = True)
	ratings = db.Column(db.Integer, nullable = True)
	users = db.relationship('UsersModel')
	payment = db.relationship('PaymentModel')
	promo = db.relationship('PromoCodeModel')
	address = db.relationship('UsersAddressModel')
	menuorderitem = db.relationship('MenuOrderItemModel', lazy = 'dynamic')



	def __init__(order_id, user_id, payment_id, address_id, promo_code, special_note, ratings):

		self.order_id = order_id
		self.user_id = user_id
		self.payment_id = payment_id
		self.address_id = address_idb  
		self.promo_code = promo_code
		self.special_note = special_note
		self.ratings = ratings


	def json(self):
		return {'order_id': self.order_id, 'user_id': self.user_id, 'payment_id': self.payment_id, 'address_id': self.address_id, 'promo_code': self.promo_code, 'special_note': self.special_note, 'ratings': self.ratings}

	@classmethod
	def find_by_id(cls, id):
		return cls.query.filter_by(id = id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

