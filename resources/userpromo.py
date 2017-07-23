from flask_restful import Resource, reqparse
from flask import request
from models.userpromo import UserPromoModel
from flask_restful_swagger import swagger
from datetime import datetime


class UserPromoEdit(Resource):

	@swagger.operation(
		notes='Get User Promo Code',
		nickname='GET',
		parameters=[
			{
				"name": "userpromo_id",
				"required": True,
				"dataType": "int"
			}]
		)
	def get(self, userpromo_id):

		userpromo = UserPromoModel.query.filter_by(userpromo_id = userpromo_id).first()
		if userpromo:
			return {'data': {'status':True, 'promo': userpromo.json()}}

	@swagger.operation(
		notes='Edit User Promo Code When Used',
		nickname='PUT',
		parameters=[
			{
				"name": "userpromo_id",
				"required": True,
				"dataType": "int"
			}]
		)

	def put(self, userpromo_id):
		userpromo = UserPromoModel.query.filter_by(userpromo_id = userpromo_id).first()

		if userpromo:
			userpromo.userpromo_used = True
			userpromo.save_to_db()
			return {'data': {'status': True,'promo': userpromo.json()}}
		return {'data': {'status': False}}

class UserPromo(Resource):



	@swagger.operation(
		notes='Get Users UnUsed Promo Code',
		nickname='GET',
		parameters=[
			{
				"name": "user_id",
				"required": True,
				"dataType": "int"
			}]
		)
	def get(self, user_id):

		return {'data': [item.json() for item in UserPromoModel.query.filter_by(user_id = user_id, userpromo_used = True).all()]}

