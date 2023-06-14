import datetime
import io
import os
from flask import Blueprint, flash, redirect, request, url_for, send_file
from flask import render_template, current_app
from werkzeug.utils import secure_filename
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

    possible_clients = {}  # {lawyer_id: [involved, ...]}
    for i in case.involved:
        if i.role.is_lawyer():
            possible_clients[i.id] = []
            for j in case.involved:
                if j.role.is_client():
                    allready_client = False
                    for k in i.clients:
                        if j.id == k.id:
                            allready_client = True
                    if not allready_client:
                        possible_clients[i.id].append(j)

    if form.validate_on_submit():
        pass
    return render_template(
        "edit_case_involved.html",
        case=case,
        form=form,
        possible_clients=possible_clients,
    )


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
    "/cases/<int:case_id>/edit/involved/<int:lawyer_id>/clients/<int:client_id>/remove",
    methods=["GET", "POST"],
)
def remove_client_from_lawyer(case_id, lawyer_id, client_id):
    inv = db.session.query(Involved).get_or_404(lawyer_id)
    client = db.session.query(Involved).get_or_404(client_id)
    # check if they belong to case_id
    if inv.case_id != case_id or client.case_id != case_id:
        flash("Die Personen gehören nicht zu diesem Fall.", "warning")
        return redirect(url_for("cases.edit_case_involved", case_id=case_id))
    # check if client is in list of clients of lawyer
    if client not in inv.clients:
        flash("Der Klient ist nicht in der Liste des Anwalts.", "warning")
        return redirect(url_for("cases.edit_case_involved", case_id=case_id))
    inv.clients.remove(client)
    db.session.commit()
    flash("Der Klient wurde erfolgreich entfernt.", "success")
    return redirect(url_for("cases.edit_case_involved", case_id=case_id))


@cases.route(
    "/cases/<int:case_id>/edit/involved/<int:lawyer_id>/clients/<int:client_id>/add",
    methods=["GET", "POST"],
)
def add_client_to_lawyer(case_id, lawyer_id, client_id):
    inv = db.session.query(Involved).get_or_404(lawyer_id)
    client = db.session.query(Involved).get_or_404(client_id)
    # check if they belong to case_id
    if inv.case_id != case_id or client.case_id != case_id:
        print("case_id", case_id)
        flash("Die Personen gehören nicht zu diesem Fall.", "warning")
        return redirect(url_for("cases.edit_case_involved", case_id=case_id))
    # check if client is in list of clients of lawyer
    if client in inv.clients:
        print("client in inv.clients")
        flash("Der Klient ist bereits in der Liste des Anwalts.", "warning")
        return redirect(url_for("cases.edit_case_involved", case_id=case_id))
    inv.clients.append(client)
    db.session.commit()
    flash("Der Klient wurde erfolgreich hinzugefügt.", "success")
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


@cases.route("/cases/<int:case_id>/edit/documents", methods=["GET", "POST"])
def edit_case_documents(case_id):
    form = UploadDocumentForm()
    case = db.session.query(Case).get_or_404(case_id)
    documets = case.documents
    print("documets", documets)
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        path = os.path.join(
            current_app.instance_path, str(case_id), "documents", filename
        )
        os.makedirs(os.path.dirname(path), exist_ok=True)
        f.save(path)
        print("path", path)
        doc = Document(
            name=filename,
            path=path,
            case_id=case_id,
            date=datetime.datetime.now(),
            description=form.description.data,
        )
        db.session.add(doc)
        db.session.commit()
        flash("Das Dokument wurde erfolgreich hochgeladen.", "success")
        return redirect(url_for("cases.edit_case_documents", case_id=case_id))
    return render_template(
        "edit_case_documents.html",
        case=case,
        documents=documets,
        form=form,
    )


@cases.route("/cases/<int:case_id>/edit/documents/download/<int:document_id>")
def download_document(case_id, document_id):
    doc = db.session.query(Document).get_or_404(document_id)
    path = doc.path
    if not os.path.exists(path):
        flash("Das Dokument existiert nicht mehr.", "warning")
        return redirect(url_for("cases.edit_case_documents", case_id=case_id))
    return send_file(
        path,
        as_attachment=True,
    )


@cases.route(
    "/cases/<int:case_id>/edit/documents/delete/<int:document_id>", methods=["POST"]
)
def delete_document(case_id, document_id):
    doc = db.session.query(Document).get_or_404(document_id)
    path = doc.path
    if not os.path.exists(path):
        flash("Das Dokument existiert nicht mehr.", "warning")
        return redirect(url_for("cases.edit_case_documents", case_id=case_id))
    os.remove(path)
    db.session.delete(doc)
    db.session.commit()
    flash("Das Dokument wurde erfolgreich gelöscht.", "success")
    return redirect(url_for("cases.edit_case_documents", case_id=case_id))


@cases.route(
    "/cases/<int:case_id>/edit/trials/",
    methods=["GET", "POST"],
)
def edit_case_trials(case_id):
    form = CreateTrialForm()
    case = db.session.query(Case).get_or_404(case_id)
    if form.validate_on_submit():
        trial = Trial(
            date=form.date.data,
            description=form.description.data,
            case_id=case_id,
            name=form.name.data,
        )
        db.session.add(trial)
        if form.use_address.data == True:
            a = Address(
                city=form.city.data,
                street=form.street.data,
                house_number=form.house_number.data,
                zip_code=form.zip_code.data,
                country=form.country.data,
            )
            db.session.add(a)
            trial.address = a
        db.session.commit()
        print("trial", trial)
        print(
            "Es wurde eine Adresse angelegt."
            if form.use_address.data
            else "Keine neue Adresse angelegt!"
        )
        flash("Die Verhandlung wurde erfolgreich angelegt.", "success")
        return redirect(
            url_for(
                "cases.edit_case_trial_attendees", case_id=case_id, trial_id=trial.id
            )
        )

    return render_template(
        "edit_case_trials.html",
        case=case,
        form=form,
    )


@cases.route(
    "/cases/<int:case_id>/edit/trials/<int:trial_id>/attendees",
    methods=["GET", "POST"],
)
def edit_case_trial_attendees(case_id, trial_id):
    form = AddAttendeeForm()
    trial = db.session.query(Trial).get_or_404(trial_id)
    attendees = trial.attendees
    return render_template(
        "edit_case_trial_attendees.html",
        trial=trial,
        attendees=attendees,
        form=form,
        case=trial.case,
    )


@cases.route(
    "/cases/<int:case_id>/edit/trials/<int:trial_id>/attendees/<int:involved_id>/add",
    methods=["POST"],
)
def add_attendee_to_trial(case_id, trial_id, involved_id):
    print("case_id")
    trial = db.session.query(Trial).get(trial_id)
    inv = db.session.query(Involved).get(involved_id)
    print("inv", inv)
    if inv.case_id != case_id:
        flash("Die Person gehört nicht zu diesem Fall.", "warning")
        return redirect(
            url_for(
                "cases.edit_case_trial_attendees", case_id=case_id, trial_id=trial_id
            )
        )
    if inv in trial.attendees:
        flash("Die Person ist bereits in der Liste der Teilnehmer.", "warning")
        return redirect(
            url_for(
                "cases.edit_case_trial_attendees", case_id=case_id, trial_id=trial_id
            )
        )
    trial.attendees.append(inv)
    db.session.commit()
    flash("Die Person wurde erfolgreich hinzugefügt.", "success")
    return redirect(
        url_for("cases.edit_case_trial_attendees", case_id=case_id, trial_id=trial_id)
    )


@cases.route(
    "/cases/<int:case_id>/edit/trials/<int:trial_id>/attendees/<int:involved_id>/remove",
    methods=["POST"],
)
def remove_attendee_from_trial(case_id, trial_id, involved_id):
    trial = db.session.query(Trial).get_or_404(trial_id)
    inv = db.session.query(Involved).get_or_404(involved_id)
    if inv.case_id != case_id:
        flash("Die Person gehört nicht zu diesem Fall.", "warning")
        return redirect(
            url_for(
                "cases.edit_case_trial_attendees", case_id=case_id, trial_id=trial_id
            )
        )
    if inv not in trial.attendees:
        flash("Die Person ist nicht in der Liste der Teilnehmer.", "warning")
        return redirect(
            url_for(
                "cases.edit_case_trial_attendees", case_id=case_id, trial_id=trial_id
            )
        )
    trial.attendees.remove(inv)
    db.session.commit()
    flash("Die Person wurde erfolgreich entfernt.", "success")
    return redirect(
        url_for("cases.edit_case_trial_attendees", case_id=case_id, trial_id=trial_id)
    )


@cases.route(
    "/cases/create/",
    methods=["GET", "POST"],
)
def create_case():
    form = CreateCaseForm()
    if form.validate_on_submit():
        case = Case(name=form.name.data, description=form.description.data)
        db.session.add(case)
        db.session.commit()
        flash("Der Fall wurde erfolgreich angelegt.", "success")
        return redirect(url_for("cases.edit_case_involved", case_id=case.id))
    return render_template("create_case.html", form=form)


# delete case
@cases.route(
    "/cases/<int:case_id>/delete/",
    methods=["POST"],
)
def delete_case(case_id):
    case = db.session.query(Case).get_or_404(case_id)
    db.session.delete(case)
    db.session.commit()
    flash("Der Fall wurde erfolgreich gelöscht.", "success")
    return redirect(url_for("cases.cases_page"))
