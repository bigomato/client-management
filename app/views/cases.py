from flask import Blueprint, flash, redirect, request, url_for
from flask import render_template
from sqlalchemy import or_
from app import db
from app.models.models import *
from app.views.case_forms import *

cases = Blueprint("cases", __name__)


@cases.route("/cases")
def cases_page():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str)
    select = db.session.query(Case)
    if search != "":
        select = select.filter(
            or_(
                Case.name.like(f"%{search}%"),
                Case.description.like(f"%{search}%"),
            )
        )
    cases = db.paginate(select, page=page, per_page=16, error_out=False)
    if search != "" and cases.total == 0:
        flash("Es wurden keine Fälle, die auf Ihre Suche passen, gefunden.", "warning")
        return redirect(url_for("cases.cases_page", page=1, s=""))
    if page > cases.pages:
        return redirect(url_for("cases.cases_page", page=cases.pages))
    return render_template(
        "cases.html", CaseStatus=CaseStatus, cases=cases, search=search
    )


@cases.route("/cases/<int:case_id>")
def case(case_id):
    case = db.session.query(Case).get_or_404(case_id)
    return render_template("case.html", case=case, CaseStatus=CaseStatus)


@cases.route("/cases/<int:case_id>/edit", methods=["GET", "POST"])
def edit_case_details(case_id):
    form = EditCaseFrom()
    case = db.session.query(Case).get_or_404(case_id)
    if form.validate_on_submit():
        case.name = form.name.data
        case.description = form.description.data
        case.case_status = form.case_status.data
        db.session.commit()
        flash("Der Fall wurde erfolgreich bearbeitet.", "success")
    form.name.data = case.name
    form.description.data = case.description
    form.case_status.data = case.case_status
    return render_template(
        "edit_case_datail.html", case=case, CaseStatus=CaseStatus, form=form
    )


@cases.route("/cases/<int:case_id>/edit/involved", methods=["GET", "POST"])
def edit_case_involved(case_id):
    form = AddInvolvedPerson()
    persons = db.session.query(Person).filter(
        Person.id.notin_(
            db.session.query(Involved.person_id).filter(Involved.case_id == case_id)
        )
    )
    form.person.choices = [(person.id, str(person)) for person in persons]
    form.role.choices = [(role.name, role.display()) for role in InvolvementRole]
    case = db.session.query(Case).get_or_404(case_id)

    if form.validate_on_submit():
        pass
    return render_template("edit_case_involved.html", case=case, form=form)


@cases.route("/cases/<int:case_id>/edit/involved/add", methods=["POST"])
def add_involved_person(case_id):
    form = AddInvolvedPerson()
    persons = db.session.query(Person).filter(
        Person.id.notin_(
            db.session.query(Involved.person_id).filter(Involved.case_id == case_id)
        )
    )
    form.person.choices = [(person.id, str(person)) for person in persons]
    form.role.choices = [(role.name, role.display()) for role in InvolvementRole]

    if form.validate_on_submit():
        inv = Involved(
            person_id=form.person.data,
            case_id=case_id,
            role=form.role.data,
        )
        db.session.add(inv)
        db.session.commit()
        flash("Die Person wurde erfolgreich hinzugefügt.", "success")

    return redirect(url_for("cases.edit_case_involved", case_id=case_id))


@cases.route(
    "/cases/<int:case_id>/edit/involved/<int:involved_id>/remove", methods=["POST"]
)
def remove_involved_person(case_id, involved_id):
    inv = db.session.query(Involved).get_or_404(involved_id)
    db.session.delete(inv)
    db.session.commit()
    flash("Die Person wurde erfolgreich entfernt.", "success")
    return redirect(url_for("cases.edit_case_involved", case_id=case_id))
