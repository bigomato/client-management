from flask import Blueprint, flash, redirect, request, url_for
from flask import render_template
from sqlalchemy import or_
from app import db
from app.models.models import *
from datetime import datetime

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


@clients.route("/clients/create", methods=["GET", "POST"])
def create_client():
    if request.method == "POST":
        a = Address(
            city=request.form.get("city"),
            street=request.form.get("street"),
            house_number=request.form.get("house_number"),
            zip_code=request.form.get("zip_code"),
            country=request.form.get("country"),
        )

        p = Person(
            name=request.form.get("name"),
            surname=request.form.get("surname"),
            birthdate=datetime.strptime(request.form.get("birthdate"), "%Y-%m-%d"),
            our_client=True,
            address=a,
        )

        ci = ContactInfo(
            phone_number=request.form.get("phone_number"),
            email=request.form.get("email"),
            person=p,
        )
        db.session.add_all([a, p, ci])
        db.session.commit()
    return render_template("create_client.html")
