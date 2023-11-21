from flask import Flask
from api.auth import auth
from api.views import views
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'the_secret_key_is_nothing'

    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(views)
    from api.models import User

    manager = LoginManager()
    manager.login_view = 'auth.login'
    manager.init_app(app)

    @manager.user_loader
    def load_user(id):
        return User.objects(id=id).first()
    return app