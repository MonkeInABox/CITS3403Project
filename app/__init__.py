from flask import Flask, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import requests

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models

def verify_captcha(captcha_response):
    if not captcha_response:
        return False, "Please enter the CAPTCHA field."

    captcha_data = {
        'secret': current_app.config['RECAPTCHA_PRIVATE_KEY'],
        'response': captcha_response
    }
    captcha_verification = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captcha_data)
    verification_result = captcha_verification.json()

    if not verification_result['success']:
        return False, "CAPTCHA verification failed. Please try again."

    return True, None

