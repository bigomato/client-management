from flask import Blueprint, flash, redirect, request, url_for
from flask import render_template
from sqlalchemy import or_
from app import db
from app.models.models import *
from datetime import datetime
from app.views.person_forms import *


persons = Blueprint("persons", __name__)


@persons.route("/persons/create", methods=["GET", "POST"])
def create_person():
    type = request.args.get("type")
    form = CreatePersonForm()
    if form.validate_on_submit():
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
            our_client=True if request.form.get("lawyer_or_client")=="client" else False,
            our_lawyer=True if request.form.get("lawyer_or_client")=="lawyer" else False,
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

    return render_template("create_person.html", form=form, type=type)
