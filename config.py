import os
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/kmnorth'
SQLALCHEMY_DATABASE_URI ='mysql+pymysql://akki7272:akki7272@fooddelivery.ceckddzhbyhp.us-west-2.rds.amazonaws.com:3306/kmnorth2'

#  application.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://kmnorth7272:kmnorth7272@kmnorth-cluster.cluster-cjyjj0rgxaie.us-west-2.rds.amazonaws.com:3306/kmnorth'
# application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')