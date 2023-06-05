from flask import Blueprint, flash, redirect, request, url_for
from flask import render_template
from sqlalchemy import or_
from app import db
from app.models.models import *
from datetime import datetime
from app.views.client_forms import *

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
    type = request.args.get("type")
    form = CreateClientForm()
    if request.form.get("lawyer_or_client") == "client" and form.validate_on_submit():
        print("Hi")
        a = Address(
            city=form.city.data,
            street=form.street.data,
            house_number=form.house_number.data,
            zip_code=form.zip_code.data,
            country=form.country.data,
        )

        p = Person(
            name=form.name.data,
            surname=form.surname.data,
            birthdate=form.birthdate.data,
            our_client=True,
            address=a,
        )

        ci = ContactInfo(
            phone_number=form.phone_number.data,
            email=form.email.data,
            person=p,
        )

        print("a, p, ci", a, p, ci)
        db.session.add_all([a, p, ci])
        db.session.commit()
        print("a, p, ci", a, p, ci)

    elif request.form.get("lawyer_or_client") == "lawyer" and form.validate_on_submit():
        a = Address(
            city=form.city.data,
            street=form.street.data,
            house_number=form.house_number.data,
            zip_code=form.zip_code.data,
            country=form.country.data,
        )

        p = Person(
            name=form.name.data,
            surname=form.surname.data,
            birthdate=form.birthdate.data,
            our_lawyer=True,
            address=a,
        )

        ci = ContactInfo(
            phone_number=form.phone_number.data,
            email=form.email.data,
            person=p,
        )

        print("a, p, ci", a, p, ci)
        db.session.add_all([a, p, ci])
        db.session.commit()
        print("a, p, ci", a, p, ci)

    return render_template("create_client.html", form=form, type=type)
