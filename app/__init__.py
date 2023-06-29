from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    db.init_app(app)
    migrate.init_app(app, db)

    from app import views

    app.register_blueprint(views.employee_api)

    return app
