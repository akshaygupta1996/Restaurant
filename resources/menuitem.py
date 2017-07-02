from flask_restful import Resource, reqparse
from flask import request
from models.menuitem import MenuItemModel
from flask_restful_swagger import swagger
from flask_restful_swagger import swagger


class MenuItem(Resource):
	
	parser = reqparse.RequestParser()
	parser.add_argument('name',
			type = str,
			required = True,
			help = "Menu Name Required")
	parser.add_argument('description',
			type = str,
			required = True,
			help = "If No Description send empty String")
	parser.add_argument('full_price',
			type = int,
			required = True,
			help = "Price is Required")
	parser.add_argument('half_price',
			type = int,
			required = False)
	parser.add_argument('cat_id',
			type = int,
			required = True,
			help = "Category To which this item belongs is required")

	@swagger.operation(
		notes='Adding A Menu Item',
		nickname='POST',
		parameters=[
			{
				"name": "name",
				"required": True,
				"dataType": "string"
			},
			{
				"name": "description",
				"required": True,
				"dataType":"string"
			},
			{
				"name": "full_price",
				"required": True,
				"dataType": "int"
			},
			{
				"name": "half_price",
				"required": False,
				"dataType": "int"
			},
			{
				"name": "cat_id",
				"required": True,
				"dataType": "int"
			}
			]
		)

	def post(self):

		data = MenuItem.parser.parse_args()

		if data['half_price'] is not None:
			item = MenuItemModel(data['name'], data['description'], data['full_price'], data['half_price'], data['cat_id'])
		else:
			item = MenuItemModel(data['name'], data['description'], data['full_price'],None, data['cat_id'])

		try:
			item.save_to_db()
		except:
			return {"status": False, 'message': 'Error Occured'}, 500
		
		return {'status': True, 'data': item.json()}, 201




class MenuItemEdit(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('name',
			type = str,
			required = True,
			help = "Menu Name Required")

	parser.add_argument('description',
			type = str,
			required = False)
	parser.add_argument('full_price',
			type = int,
			required = True,
			help = "Price is Required")
	parser.add_argument('half_price',
			type = int,
			required = False)
	parser.add_argument('cat_id',
			type = int,
			required = True,
			help = "Category To which this item belongs is required")

	@swagger.operation(
		notes='Get a Menu Item',
		nickname='GET',
		parameters=[
			{
				"name": "id",
				"required": True,
				"dataType": "int"
			}]
		)
	def get(self, id):

		item = MenuItemModel.find_by_id(id)
		if item:
			return {'status': True, 'data': item.json()}
		return {'status': False}

	@swagger.operation(
		notes='Edit a Menu Item',
		nickname='PUT',
		parameters=[
			{
				"name": "id",
				"required": True,
				"dataType": "int"
			}]
		)
	def put(self, id):

		data = MenuItemEdit.parser.parse_args()
		item = MenuItemModel.find_by_id(id)
		if item:
			item.name = data['name']
			item.description = data['description']
			item.full_price = data['full_price']
			if data['half_price'] is not None:
				item.half_price = data['half_price']
			else:
				item.half_price = None
			item.cat_id = data['cat_id']
			item.save_to_db()
			return {'status': True, 'data': item.json()}

		return {'status': False}

	@swagger.operation(
		notes='Delete a Menu Item',
		nickname='DELETE',
		parameters=[
			{
				"name": "id",
				"required": True,
				"dataType": "int"
			}]
		)

	def delete(self, id):

		item = MenuItemModel.find_by_id(id)
		if item:
			item.delete_from_db()
			return {'status': True}
		return {'status': False}
		








