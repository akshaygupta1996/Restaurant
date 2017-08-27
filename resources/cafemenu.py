from flask_restful import Resource, reqparse
from flask import request
from models.cafemenu import CafeMenuOrder
from models.cafemenuitems import CafeMenuItemsModel
from flask_restful_swagger import swagger
from pyfcm import FCMNotification
import json
import datetime
from db import db
from flask import jsonify
import pyrebase
import pytz

# config = {
#   "apiKey": "AIzaSyAkC3R1awnMDNSfSbYwFvOPkgO5mtnT1Dg",
#   "authDomain": "kmnorth-39c42.firebaseapp.com",
#   "databaseURL": "https://kmnorth-39c42.firebaseio.com",
#   "storageBucket": "gs://kmnorth-39c42.appspot.com"
# }

class CafeMenuResorce(Resource):

	parser = reqparse.RequestParser()

	parser.add_argument('payment',
			type = bool,
			required = True,
			help = "Payment Done Not Done")
	parser.add_argument('subtotal',
			type=int,
			required = True,
			help = "Total Amount Required")
	parser.add_argument('tax',
			type = float,
			required = True,
			help = "Amount Tax Required")
	parser.add_argument('total',
			type = float,
			required = True,
			help = "Total Amount Required")
	parser.add_argument('menu',
			type = str,
			required = True,
			help = "menu Array Required")


	def post(self):

		# db.session.begin(subtransactions=True)

		try:

				data = CafeMenuResorce.parser.parse_args()

				order_id = CafeMenuOrder.getOrderNumber()

				print data['menu']




				order = CafeMenuOrder(order_id, data['payment'], data['subtotal'], data['tax'], data['total'])
				try:
					# order.save_to_db()
					print "Try Block"
					db.session.add(order)
					db.session.flush()
					# db.session.commit()
				except:
					return {'data':{"status": False, "message": "Order Failed"}}, 500


				o_id = order.id
				print o_id

				menu = json.loads(data['menu'])
				print menu
				print len(menu)

				for m in menu:

					print m
					print o_id
					print m["menu_id"]
					print m["menu_qty"]
					print m["menu_amount"]
					print m["menu_choice"]
					# m = json.loads(me)

					mmodel = CafeMenuItemsModel(o_id, m['menu_id'], m['menu_qty'],m['menu_amount'], m['menu_choice'])

					try:
						# mmodel.save_to_db()
						#print "Menu Try Block"
						db.session.add(mmodel)
						db.session.flush()
						# db.session.commit()
					except:
						return {'data':{"status": False, "message": "Menu Item Save Failed"}}, 500

				db.session.commit()
				# push_service = FCMNotification(api_key="AAAABnCMzP4:APA91bHf4jst14Er5BrZMC9fOVVRGtMUVkPF7VYUI8t3BWbReJJbH_KYui8TIjITnTGZTq8HoKRPztnBsSXAD07m-JA1Tv1Wf6-I4P8gy3coaeMzJpG2K2alBF9iOHJQjbtQhjXuxzFo")
 
				# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging
				# firebase = pyrebase.initialize_app(config)
				# dbfirebase = firebase.database()
				# data = {"order": order.json(), "menu": menu, "datetime": str(datetime.datetime.now(pytz.timezone('Asia/Calcutta')))}
				# dbfirebase.child("cafeorders").child(str(order_id)).set(data)
				# admin = AdminModel.find_by_username("admin")
				# print admin.fcmtoken
				# registration_id = admin.fcmtoken
				# message_title = "New Order"
				# message_body = "A new Cafe Food order has arrived..!! Confirm the order "
				# push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
 
				return {'data': {"status": True, "order": order.json() ,"menu": menu}}
		# except:
		# 	db.session.rollback()
		finally:
			db.session.close()



class CafePaymentDone(Resource):


	def put(self, order_id):

			order = CafeMenuOrder.find_by_code(order_id)
			if order:
				order.payment = True
				order.save_to_db()

				return {"data": {"status": True}}

			return {"data": {"status": False}}

