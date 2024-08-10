from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from .celery_utils import make_celery

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.login_message_category = 'info'
mail = Mail()
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    # celery = make_celery(app)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    celery = make_celery(app)
    print(f"celery : {celery}")
    app.celery = celery
    with app.app_context():
        db.create_all()

    from app.routes import main
    app.register_blueprint(main)

    return app,celery
