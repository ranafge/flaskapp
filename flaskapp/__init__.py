from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskapp.config import Config
from flaskapp import config


db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()
login.login_view = 'users.login'
migrate = Migrate()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    from flaskapp.models import db
    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from flaskapp.users.routes import users
    from flaskapp.posts.routes import posts
    from flaskapp.main.routes import main
    from flaskapp.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app




