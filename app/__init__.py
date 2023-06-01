from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
    app.config["POPULATE_DATABASE"] = True

    db.init_app(app)
    from .views.main import main
    from .views.clients import clients
    from .views.lawyers import lawyers
    from .views.cases import cases

    app.register_blueprint(main)
    app.register_blueprint(clients)
    app.register_blueprint(lawyers)
    app.register_blueprint(cases)
    from app.models.models import (
        attends,
        representing,
        Person,
        Address,
        ContactInfo,
        Case,
        Trial,
        Involved,
        Document,
        Judgement,
    )

    with app.app_context():
        if app.config["POPULATE_DATABASE"]:
            db.drop_all()
            db.create_all()
            from app.populate_db import populate_db

            print("*** Populating database ***")
            populate_db()
            print("*** Database populated ***")
        else:
            db.create_all()

    return app
