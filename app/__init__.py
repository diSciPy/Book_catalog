import os
from flask import Flask, g, request, redirect, session
from flask_sso import SSO
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import dev
from flask_babel import Babel, _
from flask_wtf.csrf import CSRFProtect
import psycopg2
from pathlib import Path

SECRET_KEY = os.urandom(32)
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'authentication.do_the_login'
login_manager.session_protection = 'strong'
bcrypt = Bcrypt()


def create_app(config_type):  # dev,test or prod
    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')

    app.config.from_pyfile(configuration)
    db.init_app(app)  # bind database to flask
    #conn = psycopg2.connect(DATABASE_URI, sslmode='require')
    bootstrap.init_app(app)  # initialize bootstrap
    login_manager.init_app(app)  # initialize log.manage
    bcrypt.init_app(app)  # initialize bcrypt
    csrf = CSRFProtect(app) #initialize CSRF protection
    csrf.init_app(app)
    app.config['SECRET_KEY'] = SECRET_KEY


    from app.catalog import main  # import blueprint
    app.register_blueprint(main)  # register blueprint

    from app.authentication import authentication
    app.register_blueprint(authentication)

    from app.landing_page import landing_page
    app.register_blueprint(landing_page)

    # set up Babel
    babel = Babel(app)
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.getenv('BABEL_TRANSLATION_DIRECTORIES', './locale')

    @babel.localeselector
    def get_locale():
        if not g.get('lang_code', None):
            g.lang_code = request.accept_languages.best_match(app.config['LANGUAGES'])
        return g.lang_code

    return app


def get_project_root() -> Path:
    return Path(__file__).parent
