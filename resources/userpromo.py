from flask_restful import Resource, reqparse
from flask import request
from models.userpromo import UserPromoModel
from models.promocode import PromoCodeModel
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



class CheckPromoAvailability(Resource):


	def get(self, promo_code, user_id):

		date = datetime.now().date()

		promocode = PromoCodeModel.query.filter_by(promo_code = promo_code).first()

		if promocode:
			if promocode.promo_validity >= date:

				if promocode.promo_user == False:

					return {'date': { 'status': True, 'promocode': promocode.json()}}
				else:

					checkuser = UserPromoModel.query.filter(UserPromoModel.user_id == user_id, UserPromoModel.promo_code == promo_code).first()
					if checkuser is None:
						return {'data': {'status': False}}
					else:
						if checkuser.userpromo_used == False and checkuser.userpromo_validity >= date:
							return {'date': { 'status': True, 'promocode': promocode.json()}}
		
	
		return {'data':{'status': False}}



