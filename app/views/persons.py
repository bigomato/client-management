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
    case_id = request.args.get("case_id")
    case = Case.query.filter_by(id=case_id).first()
    role = request.args.get("role")
    if not case and case_id not in ["", None]:
        flash(
            "Du hast versucht eine Person zu einem Fall hinzuzufügen, der nicht existiert.",
            "danger",
        )
        return redirect(url_for("cases.cases_page"))
    if case and not role:
        flash(
            "Du hast versucht eine Person zu einem Fall hinzuzufügen, ohne eine Rolle anzugeben.",
            "danger",
        )
        return redirect(url_for("cases.edit_case_involved", case_id=case_id))
    # check if the role is valid using the Enum
    if case and role not in [role.name for role in InvolvementRole]:
        flash(
            "Du hast versucht eine Person zu einem Fall hinzuzufügen, mit einer ungültigen Rolle.",
            "danger",
        )
        return redirect(url_for("cases.edit_case_involved", case_id=case_id))
    if form.validate_on_submit():
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
            our_client=True
            if request.form.get("lawyer_or_client") == "client"
            else False,
            our_lawyer=True
            if request.form.get("lawyer_or_client") == "lawyer"
            else False,
            address=a,
        )

        ci = ContactInfo(
            phone_number=form.phone_number.data,
            email=form.email.data,
            person=p,
        )

        # check if they wanted to add a person to a case
        if case_id != "":
            inv = Involved(
                case_id=case_id,
                person=p,
                role=role,
            )
            db.session.add(inv)

        db.session.add_all([a, p, ci])
        db.session.commit()

        if case_id != "":
            flash("Die Person wurde erfolgreich hinzugefügt.", "success")
            return redirect(url_for("cases.edit_case_involved", case_id=case_id))

    return render_template("create_person.html", form=form, type=type)
