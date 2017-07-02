from flask_restful import Resource, reqparse
from flask import request
from models.users import UsersModel
from flask_restful_swagger import swagger

class Users(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('fname',
			type = str,
			required = True,
			help = "First Name is Required"
			)
	parser.add_argument('lname',
			type = str,
			required = True,
			help = "Last Name is Required")
	parser.add_argument('phone_number',
			type = str,
			required = True,
			help = "Phone Number Required")
	parser.add_argument('email',
			type = str,
			required = True,
			help = "Email Required")
	parser.add_argument('password',
		type = str,
		required = True,
		help = "Password Required")
	@swagger.operation(
		notes = "Get All Registered Users",
		nickname='GET')

	def get(self):

		return {'users': [user.json() for user in UsersModel.query.all()]}

	
	@swagger.operation(
		notes='Register a User',
		nickname='POST',
		parameters=[
			{
				"name": "fname",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "lname",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "email",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "phone_number",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "password",
				"required": True,
				"dataType": "String"
			}

		])
	def post(self):

		data = Users.parser.parse_args()

		if UsersModel.find_by_email(data['email']):
			return {'error': "Email Already Regsitered"}, 400

		if UsersModel.find_by_phone(data['phone_number']):
			return {'error': "Phone Number Already Registered"}, 400

		user = UsersModel(data['fname'], data['lname'], data['email'], data['phone_number'], data['password'])

		try:
			user.save_to_db()
		except:
			return {'message': "An Error Occured"}, 500

		return user.json(), 201
		

class LoginUsers(Resource):

		@swagger.operation(
			notes='Login User',
			nickname='GET',
			parameters=[
			{
				"name": "flag",
				"required": True,
				"dataType": "INT",
				"description": "0 for Email and 1 for Phone"
			},
			{
				"name": "user_ep",
				"required": True,
				"dataType": "String",
				"description": "If flag 0 then pass email else phone_number"
			},
			{
				"name": "password",
				"required": True,
				"dataType": "String"
			}

		])

		def get(self, flag, user_ep,password):

			if flag == 0:
				user_email = UsersModel.find_by_email(user_ep)
				if user_email:
					if user_email.password == password:
						return user_email.json()
			if flag == 1:
				user_phone = UsersModel.find_by_phone(user_ep)
				if user_phone:
					if user_phone.password == password:
						return user_phone.json()
		
			return {'error': 'Authentication Error'}, 404


