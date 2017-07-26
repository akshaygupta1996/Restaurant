from flask_restful import Resource, reqparse
from flask import request
from models.menuorder import MenuOrderModel
from models.menuorderitems import MenuOrderItemModel
from models.payment import PaymentModel
from flask_restful_swagger import swagger
import json
from db import db
from flask import jsonify


class MenuOrderResource(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('user_id',
			type = int,
			required = True,
			help = "User Id is required"
		)
	parser.add_argument('address_id',
			type = int,
			required = True,
			help = "Address Required")
	parser.add_argument('promo_code',
			type=str,
			required = True,
			help = "Promo Code Required")
	parser.add_argument('special_note_required',
			type = str,
			required = True,
			help = "Sepcial Note Required")
	parser.add_argument('payment_type',
			type = str,
			required = True,
			help = "Payment Type CD/OP")
	parser.add_argument('amount',
			type = int,
			required = True,
			help = "Amount Required")
	parser.add_argument('amount_payable',
			type=int,
			required = True,
			help = "Amount Payable Required")
	parser.add_argument('amount_tax',
			type = int,
			required = True,
			help = "Amount Tax Required")
	parser.add_argument('amount_discount',
			type = int,
			required = True,
			help = "Amount Discount Required")
	parser.add_argument('amount_wallet',
			type = int,
			required = True,
			help = "Amount Wallet Required")
	parser.add_argument('amount_menu',
			type = int,
			required = True,
			help = "Amount Menu Required")
	parser.add_argument('menu',
			type = str,
			required = True,
			help = "menu Array Required")
	parser.add_argument('ratings',
			type = int,
			required = False)


	def post(self):

		# db.session.begin(subtransactions=True)

		try:

			data = MenuOrderResource.parser.parse_args()

			if data['payment_type'] == "CD":
				payment = PaymentModel(data['payment_type'], "COD", data['amount'], data['amount_payable'], data['amount_tax'], data['amount_menu'], data['amount_discount'], data['amount_wallet'] )
				try:
					# payment.save_to_db()
					db.session.add(payment)
					db.session.flush()
					# db.session.commit()
				except:
					return {'data':{"status": False, "message": "Paymnet False"}}, 500

				

				# payment_id = payment.id

				order_id = MenuOrderModel.getOrderNumber()

				order = MenuOrderModel(order_id, data['user_id'],payment.id, data['address_id'],data['promo_code'],data['special_note_required'],data['ratings'],0)
				try:
					# order.save_to_db()
					db.session.add(order)
					db.session.flush()
					# db.session.commit()
				except:
					return {'data':{"status": False, "message": "Order Failed"}}, 500


				o_id = order.id

				menu = json.loads(data['menu'])

				for m in menu:
					mmodel = MenuOrderItemModel(o_id, m['menu_id'], m['menu_qty'],m['menu_amount'], m['menu_choice'])

					try:
						# mmodel.save_to_db()
						db.session.add(mmodel)
						db.session.flush()
						# db.session.commit()
					except:
						return {'data':{"status": False, "message": "Menu Item Save Failed"}}, 500

				db.session.commit()
				return {'data': {"status": True, "payment": payment.json(), "order": order.json() ,"menu": menu}}
		except:
			db.session.rollback()
		finally:
			db.session.close()





class MenuOrderResourceEdit(Resource):

 

	def put(self, order_id):

		order = MenuOrderModel.find_by_code(order_id)
		if order:
			order.approved = True
			order.save_to_db()

			return {"data": {"status": True}}

		return {"data": {"status": False}}


class MenuOrderResourceEditRatings(Resource):



	def put(self, order_id, ratings):

		order = MenuOrderModel.find_by_code(order_id)
		if order:
			order.ratings = ratings
			order.save_to_db()

			return {"data": {"status": True}}

		return {"data": {"status": False}}
	