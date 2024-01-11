import logging
from flask import Flask, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from logging.handlers import RotatingFileHandler
import os
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
from flask_babel import lazy_gettext as _l

def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

app = Flask(__name__)
app.config.from_object(Config)

#数据库对象
db = SQLAlchemy(app)
#迁移引擎对象
migrate = Migrate(app, db)
#强制用户登录
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this passage.')

mail = Mail(app)
boot = Bootstrap(app)
moment = Moment(app)
babel = Babel(app, locale_selector=get_locale)

# print('等会谁（哪个包或模块）在使用我：',__name__)
# print(app.config['SECRET_KEY'])


if not app.debug:
    # ...

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


#从app包中导入模块routes
from app import routes, models, errors

