from db import db
from flask_restful_swagger import swagger


@swagger.model
class PromoCodeModel(db.Model):

	__tablename__ = "promocode"

	promo_id = db.Column(db.Integer, primary_key = True)
	promo_code = db.Column(db.String(10), nullable = False, unique = True)
	promo_discount_per = db.Column(db.Integer, nullable = False)
	promo_validity = db.Column(db.Date, nullable = False)
	promouser = db.relationship('UserPromoModel' , lazy = 'dynamic')


	def __init__(self, promo_code, promo_discount_per, promo_validity):
		self.promo_code = promo_code
		self.promo_discount_per = promo_discount_per
		self.promo_validity = promo_validity

	def json(self):
		return {'promo_id':self.promo_id, "promo_code": self.promo_code, "promo_validity": str(self.promo_validity), "promo_discount_per": self.promo_discount_per}

	@classmethod
	def find_by_promo_code(cls, promo_code):
		return cls.query.filter_by(promo_code = promo_code).first()

	@classmethod
	def find_by_promo_id(cls, promo_id):
		return cls.query.filter_by(promo_id = promo_id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
