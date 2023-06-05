from flask import Blueprint, flash, redirect, request, url_for
from flask import render_template
from sqlalchemy import or_
from app import db
from app.models.models import *
from datetime import datetime
from app.views.person_forms import *

clients = Blueprint("clients", __name__)


@clients.route("/clients")
def clients_page():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str)
    select = db.session.query(Person).filter(Person.our_client == True)
    if search != "":
        select = select.filter(
            or_(
                Person.name.like(f"%{search}%"),
                Person.surname.like(f"%{search}%"),
                Person.birthdate.like(f"%{search}%"),
            )
        )
    clients = db.paginate(select, page=page, per_page=16, error_out=False)
    if search != "" and clients.total == 0:
        flash(
            "Es wurden keine Mandanten, die auf Ihre Suche passen, gefunden.", "warning"
        )
        return redirect(url_for("clients.clients_page", page=1, s=""))
    if page > clients.pages:
        return redirect(url_for("clients.clients_page", page=clients.pages))
    return render_template("clients.html", clients=clients, search=search)
