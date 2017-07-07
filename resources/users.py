from flask_restful import Resource, reqparse
from flask import request, jsonify,make_response
from models.users import UsersModel
from flask_restful_swagger import swagger
from db import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


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
	parser.add_argument('register_ref',
		type=str,
		required = True,
		help = "If Users does not provide Ref Code then pass 0")
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
			},
			{
				"name": "register_ref",
				"required": True,
				"dataType": "String"
			}

		])
	def post(self):

		data = Users.parser.parse_args()

		if UsersModel.find_by_email(data['email']):
			return {'data':{'status': False,
							'message': "Email Already Regsitered"}}, 201

		if UsersModel.find_by_phone(data['phone_number']):
			return {'data':{'status': False,
							'message': "Phone Number Already Registered"}}, 201
			# return {'error': "Phone Number Already Registered"}, 400

		if data['register_ref'] == "0":
			
			refcode = UsersModel.getRefCode(data['fname'])
			user = UsersModel(data['fname'], data['lname'], data['email'], data['phone_number'], data['password'],refcode, data['register_ref'],0)
			try:
				user.save_to_db()
			except:
				return {'message': "An Error Occured"}, 500

			return {'data':{'status': True}}, 201


		else:
			user_ref =  UsersModel.find_by_refcode(data['register_ref'])
			if user_ref is not None:
				no = user_ref.register_ref_no
				if no == 2:
					return {'data': {'status': False,
								'message': "User Crossed his/her Limit"}}
					#refernece code cannot be added. User crosseds the limit

				elif no < 2:
					no = no + 1
					user_ref.register_ref_no = no
					try:
						db.session.commit()
					except:
						return {'message': "An Error Occured"}, 500
					refcode = UsersModel.getRefCode(data['fname'])
					user = UsersModel(data['fname'], data['lname'], data['email'], data['phone_number'], data['password'],refcode, data['register_ref'],0)
					try:
						user.save_to_db()
					except:
						return {'message': "An Error Occured"}, 500

					return {'data':{'status': True}}, 201
			else:
				return {'data': {'status': False,
								'message': "Reference Code Invalid"}}
		

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
						# return user_email.json()
						ret = {'data':{'access_token': create_access_token(identity=user_email.id),
								 'user_id': user_email.id,
								 'fname': user_email.fname,
								 'lname': user_email.lname,
								 'email': user_email.email,
								 'phone_number': user_email.phone_number}}
   					  	return make_response(jsonify(ret), 200)
			if flag == 1:
				user_phone = UsersModel.find_by_phone(user_ep)
				if user_phone:
					if user_phone.password == password:
						# return user_phone.json()
						ret = {'data': {'access_token': create_access_token(identity=user_phone.id),
								 'user_id': user_phone.id,
								 'fname': user_phone.fname,
								 'lname': user_phone.lname,
								 'email': user_phone.email,
								 'phone_number': user_phone.phone_number}}
   					  	return make_response(jsonify(ret), 200)
		
			return {'error': 'Authentication Error'}, 404


