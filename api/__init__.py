from flask import Flask
from api.auth import auth
from api.views import views
from flask_login import LoginManager
import os
from dotenv import load_dotenv
from flask_mail import Mail

load_dotenv()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(views)
    from api.models import User

    mail = Mail(app)

    manager = LoginManager()
    manager.login_view = 'auth.login'
    manager.init_app(app)

    @manager.user_loader
    def load_user(id):
        return User.objects(id=id).first()
    return app