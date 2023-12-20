from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

#数据库对象
db = SQLAlchemy(app)
#迁移引擎对象
migrate = Migrate(app, db)
login = LoginManager(app)

# print('等会谁（哪个包或模块）在使用我：',__name__)
# print(app.config['SECRET_KEY'])


#从app包中导入模块routes
from app import routes,models