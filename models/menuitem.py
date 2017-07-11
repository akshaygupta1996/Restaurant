from db import db
from flask_restful_swagger import swagger


class MenuItemModel(db.Model):

	__tablename__ = 'menuitem'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30), nullable = False)
	description = db.Column(db.String(150))
	full_price = db.Column(db.Integer, nullable = False)
	half_price = db.Column(db.Integer, nullable = True)
	# image_path = db.Column(db.String(400))
	cat_id = db.Column(db.Integer, db.ForeignKey('menucat.id'))
	category = db.relationship('MenuCategoryModel')

	def __init__(self, name, description, full_price, half_price, cat_id):
		self.name = name
		self.description = description
		self.full_price = full_price
		self.half_price = half_price
		self.cat_id = cat_id
		# self.image_path = image_path




	def json(self):
		return {'id': self.id, 'name': self.name, 'description': self.description, 'full_price': self.full_price, 'half_price': self.half_price, 'cat_id': self.cat_id}

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def find_by_id(cls, menu_id):

		return cls.query.filter_by(id = menu_id).first()

