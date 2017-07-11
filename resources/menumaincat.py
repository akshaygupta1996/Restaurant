from flask_restful import Resource, reqparse
from flask import request
from models.menumaincat import MenuMainCategoryModel
from models.menucat import MenuCategoryModel
from flask_restful_swagger import swagger


class MenuMainCategory(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('cat_name',
			type = str,
			required = True,
			help = "Category Name is Required"
		)
	@swagger.operation(
		notes='Adding A Menu Category',
		nickname='POST',
		parameters=[
			{
				"name": "cat_name",
				"required": True,
				"dataType": "string"
			}]
		)
	def post(self):

		data = MenuMainCategory.parser.parse_args()
		menu_cat = MenuMainCategoryModel(data['cat_name'])
		try:
			menu_cat.save_to_db()
		except:
			return {'data':{"status": False, 'message': 'Error Occured'}}, 500
		
		return {'data':{'status': True, 'maincategory': menu_cat.json()}}, 201

	@swagger.operation(
		notes='Get List of all Main Menu Category',
		nickname='GET'
		)
	def get(self):

		return {'data':{'status':True, 'category': [category.json() for category in MenuMainCategoryModel.query.all()]}}


class MenuMainCategoryEdit(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('cat_name',
			type = str,
			required = True,
			help = "Category Name is Required"
		)


	@swagger.operation(
		notes='Edit A Menu Category',
		nickname='PUT',
		parameters=[
			{
				"name": "cat_name",
				"required": True,
				"dataType": "string"
			}]
		)

	def put(self, cat_id):

		data = MenuMainCategoryEdit.parser.parse_args()
		menu_cat = MenuMainCategoryModel.find_by_id(cat_id)
		if menu_cat:
			menu_cat.cat_name = data['cat_name']
			menu_cat.save_to_db()
			return {'data':{'status': True, 'data': menu_cat.json()}}

		return {'data':{'status': False, 'error': "Invalid Id"}}

	@swagger.operation(
		notes='List all sub menu Category in the category',
		nickname='GET',
		parameters=[
			{
				"name": "cat_id",
				"required": True,
				"dataType": "int"
			}]
		)

	def get(self, cat_id):
		return {'data': {'status':True, 'category':[cat.json() for cat in MenuCategoryModel.query.filter_by(main_cat_id = cat_id).all()]}}


