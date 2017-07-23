from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger
from resources.users import Users, LoginUsers
from resources.address import UserAddress, UsersAddress
from resources.menucat import MenuCategory, MenuCategoryEdit
from resources.menumaincat import MenuMainCategory, MenuMainCategoryEdit, MenuItemsByMainCategory
from resources.menuitem import MenuItem, MenuItemEdit
from resources.promocode import PromoCode, PromoCodeEdit
from resources.userpromo import UserPromo, UserPromoEdit

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from security import authenticate, identity
from flask_jwt import JWT
import os
import models
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy




# application = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))
# db = models.db


app = Flask(__name__)

db = models.db
# application.config.from_object(os.environ['APP_SETTINGS'])
# application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(application)

# application = Flask(__name__)


# @application.before_first_request
# def create_tables():
# 	db.create_all()


#application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# # 'mysql+pymysql://flaskdemo:flaskdemo@flaskdemo.cwsaehb7ywmi.us-east-1.rds.amazonaws.com:3306/flaskdemo'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/kmnorth2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://akki7272:akki7272@fooddelivery.ceckddzhbyhp.us-west-2.rds.amazonaws.com:3306/kmnorth2'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://akshay7272:akshay7272@kmnorth2.ceckddzhbyhp.us-west-2.rds.amazonaws.com:3306/km'

 # application.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://kmnorth7272:kmnorth7272@kmnorth-cluster.cluster-cjyjj0rgxaie.us-west-2.rds.amazonaws.com:3306/kmnorth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'akshay7272'
api = Api(app)
api = swagger.docs(Api(app), apiVersion='0.1')
jwt = JWTManager(app)


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
# jwt = JWT(application, authenticate, identity) # /auth
# db = SQLAlchemy(application)
# db.init_app(app)





api.add_resource(Users, '/register')
api.add_resource(LoginUsers, '/login/<int:flag>/<string:user_ep>/<string:password>')
api.add_resource(UsersAddress, '/user_address/<int:user_id>')
api.add_resource(UserAddress, '/address/<int:id>')
api.add_resource(MenuCategory, '/category/<int:main_cat_id>')
api.add_resource(MenuCategoryEdit, '/category/<int:cat_id>')
api.add_resource(MenuItem,'/menuitem')
api.add_resource(MenuItemEdit, '/menuitem/<int:id>')
api.add_resource(PromoCode,'/promocode')
api.add_resource(PromoCodeEdit,'/promocode/<int:promo_id>')
api.add_resource(UserPromoEdit,'/userpromo/<int:userpromo_id>')
api.add_resource(UserPromo,'/userpromoedit/<int:user_id>')
api.add_resource(MenuMainCategory, '/menumaincat')
api.add_resource(MenuMainCategoryEdit, '/menumaincat/<int:cat_id>')
api.add_resource(MenuItemsByMainCategory, '/menu')


if __name__ == '__main__':
	# from db import db
	db.init_app(app) 
	
	 #we are importing here due to circular imports
	manager.run()