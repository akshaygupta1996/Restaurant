from flask_restful import Resource, reqparse
from flask import request, jsonify,make_response
from models.taxes import TaxesModel
from flask_restful_swagger import swagger
from db import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


class Taxes(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('tax_name',
			type = str,
			required = True,
			help = "Tax Name is required"
			)
	parser.add_argument('tax_per',
			type = float,
			required = True,
			help = "Tax Percentage is Required")

	@swagger.operation(
		notes = "Get All Taxes",
		nickname='GET')

	def get(self):

		return {'data':{'taxes': [tax.json() for tax in TaxesModel.query.all()]}, 'status': True}


	@swagger.operation(
		notes = "Add A new Tax",
		nickname='POST',
		parameters=[
			{
				"name": "tax_name",
				"required": True,
				"dataType": "string",
				"description": "Tax Name is Required"
			},
			{
				"name": "tax_per",
				"required": True,
				"dataType": "Float",
				"description": "Tax Percentage is Required"
		}])
	def post(self):

		data = Taxes.parser.parse_args()

		tax = TaxesModel(data['tax_name'], data['tax_per'])

		try:
			tax.save_to_db()
		except:
			return {'message': "An Error Occured"}, 500
		return {'data':{'status': True, 'message': "Insert Successful"}}, 201


class TaxEdit(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('tax_name',
			type = str,
			required = True,
			help = "Tax Name is required"
			)
	parser.add_argument('tax_per',
			type = float,
			required = True,
			help = "Tax Percentage is Required")


	@swagger.operation(
		notes = "Edit A Tax",
		nickname='PUT',
		parameters=[
			{
				"name": "id",
				"required": True,
				"dataType": "int",
				"description": "Tax Id is Required"
			},
			{
				"name": "tax_name",
				"required": True,
				"dataType": "string",
				"description": "Tax Name is Required"
			},
			{
				"name": "tax_per",
				"required": True,
				"dataType": "Float",
				"description": "Tax Percentage is Required"
		}])
	def put(self, id):

		data = TaxEdit.parser.parse_args()

		tax = TaxesModel.find_by_id(id)
		if tax is not None:
			tax.tax_name = data['tax_name']
			tax.tax_per = data['tax_per']
			tax.save_to_db()
			return {'data':{'status': True, 'tax': tax.json()}}

		return {'data':{'status': False, 'error': "Invalid Id"}}




