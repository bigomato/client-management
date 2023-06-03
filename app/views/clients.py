from flask import Blueprint, redirect, request, url_for
from flask import render_template
from app import db
from app.models.models import *

clients = Blueprint("clients", __name__)


@clients.route("/clients")
def clients_page():
    page = request.args.get("page", 1, type=int)
    select = db.session.query(Person).filter(Person.our_client == True)
    clients = db.paginate(select, page=page, per_page=16, error_out=False)
    if page > clients.pages:
        return redirect(url_for("clients.clients_page", page=clients.pages))
    return render_template("clients.html", clients=clients)


@clients.route("/clients/create")
def create_client():
    return render_template("create_client.html")
