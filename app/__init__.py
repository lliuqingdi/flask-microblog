import logging
from flask import Flask, request, current_app
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
    return request.accept_languages.best_match(current_app.config['LANGUAGES'])

# app = Flask(__name__)
# app.config.from_object(Config)

#数据库对象
db = SQLAlchemy()
#迁移引擎对象
migrate = Migrate()
#强制用户登录
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this passage.')

mail = Mail()
boot = Bootstrap()
moment = Moment()
babel = Babel()
bootstrap = Bootstrap()

# print('等会谁（哪个包或模块）在使用我：',__name__)
# print(app.config['SECRET_KEY'])

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # from app.cli import bp as cli_bp
    # app.register_blueprint(cli_bp)

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')
    return app

# <-- remove errors from this import!
from app import models





