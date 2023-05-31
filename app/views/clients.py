from flask import Blueprint
from flask import render_template
from app import db
from app.models.models import *

clients = Blueprint("clients", __name__)


@clients.route("/clients")
def clients_page():
    clients = db.session.query(Person).filter(Person.our_client == True).limit(16)
    return render_template("clients.html", clients=clients)
