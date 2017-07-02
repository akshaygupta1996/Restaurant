from db import db
import datetime
from flask_restful_swagger import swagger

@swagger.model
class MenuCategoryModel(db.Model):

	__tablename__ = 'menucat'

	id = db.Column(db.Integer, primary_key = True)
	cat_name = db.Column(db.String(50), nullable=False)
	menu_items = db.relationship('MenuItemModel', lazy = 'dynamic')

	def __init__(self, cat_name):
		self.cat_name = cat_name


	def json(self):
		return { 'id': self.id, 'cat_name': self.cat_name}

	def save_to_db(self):

		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def find_by_id(cls, cat_id):

		return cls.query.filter_by(id = cat_id).first()