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
    addresses = db.session.query(Address).all()
    print("1")
    default = ("Appletree", "Keine Adresse")
    form.address.choices = [default] + [
        (address.id, str(address)) for address in addresses
    ]
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
    if case and role not in [role.name for role in InvolvementRole]:
        flash(
            "Du hast versucht eine Person zu einem Fall hinzuzufügen, mit einer ungültigen Rolle.",
            "danger",
        )
        return redirect(url_for("cases.edit_case_involved", case_id=case_id))
    print("2")
    print(form.errors)
    if form.validate_on_submit():
        print("3")
        if form.address.data != "Appletree":
            a = db.session.query(Address).get_or_404(form.address.data)
            print("using existing address")
        else:
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
        if case_id is not None:
            inv = Involved(
                case_id=case_id,
                person=p,
                role=role,
            )
            db.session.add(inv)

        db.session.add_all([a, p, ci])
        db.session.commit()

        if case_id is not None:
            flash("Die Person wurde erfolgreich hinzugefügt.", "success")
            return redirect(url_for("cases.edit_case_involved", case_id=case_id))
        else:
            flash("Die Person wurde erfolgreich hinzugefügt.", "success")
            return redirect(url_for("persons.person", person_id=p.id))
    return render_template("create_person.html", form=form, type=type)


@persons.route("/persons/<int:person_id>")
def person(person_id):
    person = db.session.query(Person).get_or_404(person_id)
    return render_template("person.html", person=person, CaseStatus=CaseStatus)


@persons.route("/persons/delete/<int:person_id>")
def delete_person(person_id):
    person = db.session.query(Person).get_or_404(person_id)
    lawyer_or_client = "lawyer" if person.our_lawyer else "client"
    db.session.delete(person)
    db.session.commit()
    flash("Die Person wurde erfolgreich gelöscht.", "success")
    if lawyer_or_client == "lawyer":
        return redirect(url_for("lawyers.lawyers_page"))
    else:
        return redirect(url_for("clients.clients_page"))
