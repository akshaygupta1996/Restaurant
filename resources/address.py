from flask_restful import Resource, reqparse
from flask import request
from models.address import UsersAddressModel
from flask_restful_swagger import swagger

class UsersAddress(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('delivery_area',
			type = str,
			required = True,
			help = "Delivery Area is Required"
			)
	parser.add_argument('address',
			type = str,
			required = True,
			help = "Address is Required")
	parser.add_argument('instructions',
			type=str,
			required = True,
			help = "Instructions Required . Else pass empty string")

	@swagger.operation(
		notes='Adding A address',
		nickname='POST',
		parameters=[
			{
				"name": "user_id",
				"required": True,
				"dataType": "int"
			},
			{
				"name": "delivery_area",
				"required": True,
				"dataType": "String",
				"description": "Get Delivery Area using Reverse GeoCoding Google Map Api"
			},
			{
				"name": "address",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "instructions",
				"required": True,
				"dataType": "String"
			}
		])
	
	def post(self, user_id):

		data = UsersAddress.parser.parse_args()
		address = UsersAddressModel(user_id, data['delivery_area'], data['address'], data['instructions'])
		try:
			address.save_to_db()
		except:
			return {"status": False, 'message': 'Error Occured'}, 500
		
		return {'status': True, 'data': address.json()}, 201

	@swagger.operation(
		notes='Getting List of Addresses of a user',
		nickname='GET',
		parameters=[
			{
				"name": "user_id",
				"required": True,
				"dataType": "int"
			}
		])
	def get(self, user_id):

		return {'address': [address.json() for address in UsersAddressModel.query.filter_by(user_id = user_id).all()]}

class UserAddress(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('delivery_area',
			type = str,
			required = True,
			help = "Delivery Area is Required"
			)
	parser.add_argument('address',
			type = str,
			required = True,
			help = "Address is Required")
	parser.add_argument('instructions',
			type=str,
			required = True,
			help = "Instructions Required . Else pass empty string")


	@swagger.operation(
		notes='Edit an Address',
		nickname='PUT',
		parameters=[
			{
				"name": "id",
				"required": True,
				"dataType": "int"
			},
			{ 
				"name": "delivery_area",
				"required": True,
				"dataType": "String",
				"description": "Get Delivery Area using Reverse GeoCoding Google Map Api"
			},
			{
				"name": "address",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "instructions",
				"required": True,
				"dataType": "String"
			}
		])

	def put(self, id):
		address = UsersAddressModel.find_by_id(id)
		if address:
			data = UserAddress.parser.parse_args()
			address.delivery_area = data['delivery_area']
			address.instructions = data['instructions']
			address.address = data['address']
			address.save_to_db()
			return {'status': True, 'data': address.json()}
		return {'status': False, 'error': "Invalid Id"}

	@swagger.operation(
		notes='Delete An address',
		nickname='DELETE',
		parameters=[
			{
				"name": "id",
				"required": True,
				"dataType": "int"
			}
		])

	def delete(self, id):
		
		address = UsersAddressModel.find_by_id(id)
		if address:
			address.delete_from_db()
			return {'status': True}

		return {'status': False, 'message': 'Address Not Deleted or Found'}



