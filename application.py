from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger
from resources.users import Users, LoginUsers
from resources.address import UserAddress, UsersAddress
from resources.menucat import MenuCategory, MenuCategoryEdit
from resources.menuitem import MenuItem, MenuItemEdit
from resources.promocode import PromoCode, PromoCodeEdit
from resources.userpromo import UserPromo, UserPromoEdit

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from security import authenticate, identity
from flask_jwt import JWT


application = Flask(__name__)




#application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# 'mysql+pymysql://flaskdemo:flaskdemo@flaskdemo.cwsaehb7ywmi.us-east-1.rds.amazonaws.com:3306/flaskdemo'
# application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/kmnorth'
application.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://kmnorth7272:kmnorth7272@kmnorth-cluster.cluster-cjyjj0rgxaie.us-west-2.rds.amazonaws.com:3306/kmnorth'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.secret_key = 'akshay7272'
api = Api(application)
api = swagger.docs(Api(application), apiVersion='0.1')
jwt = JWTManager(application)
# jwt = JWT(application, authenticate, identity) # /auth





api.add_resource(Users, '/register')
api.add_resource(LoginUsers, '/login/<int:flag>/<string:user_ep>/<string:password>')
api.add_resource(UsersAddress, '/user_address/<int:user_id>')
api.add_resource(UserAddress, '/address/<int:id>')
api.add_resource(MenuCategory, '/category')
api.add_resource(MenuCategoryEdit, '/category/<int:cat_id>')
api.add_resource(MenuItem,'/menuitem')
api.add_resource(MenuItemEdit, '/menuitem/<int:id>')
api.add_resource(PromoCode,'/promocode')
api.add_resource(PromoCodeEdit,'/promocode/<int:promo_id>')
api.add_resource(UserPromoEdit,'/userpromo/<int:userpromo_id>')
api.add_resource(UserPromo,'/userpromoedit/<int:user_id>')


if __name__ == '__main__':
	from db import db
	db.init_app(application) 
	
	 #we are importing here due to circular imports
	application.run(port=5000, debug=True)