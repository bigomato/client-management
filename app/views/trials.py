import datetime
from flask import Blueprint, flash, redirect, request, url_for, send_file
from flask import render_template, current_app
from werkzeug.utils import secure_filename
from sqlalchemy import or_
from app import db
from app.models.models import *
from app.views.trial_forms import *
from app.views.trial_forms import EditTrialForm

trials = Blueprint("trials", __name__)


@trials.route(
    "/trials/<int:trial_id>/delete",
    methods=["GET", "POST"],
)
def delete_trial(trial_id):
    trial = db.session.query(Trial).get_or_404(trial_id)
    db.session.delete(trial)
    db.session.commit()
    flash("Die Verhandlung wurde erfolgreich gelöscht.", "success")
    return redirect(url_for("cases.edit_case_trials", case_id=trial.case_id))


@trials.route(
    "/trials/<int:trial_id>/edit",
    methods=["GET", "POST"],
)
def edit_trial(trial_id):
    form = EditTrialForm()
    trial = db.session.query(Trial).get_or_404(trial_id)
    docs = db.session.query(Document).filter(Document.case_id == trial.case_id).all()
    form.document.choices = [("none", "Kein Dokument")] + [
        (doc.id, str(doc)) for doc in docs
    ]
    if form.validate_on_submit():
        trial.name = form.name.data
        trial.date = form.date.data
        trial.description = form.description.data
        if form.use_address.data:
            trial.address.country = form.country.data
            trial.address.city = form.city.data
            trial.address.zip_code = form.zip_code.data
            trial.address.street = form.street.data
            trial.address.house_number = form.house_number.data
        if trial.judgement is None:
            judgement = Judgement(
                description=form.judgement_description.data,
                judgement=form.judgement.data,
                document_id=form.document.data
                if form.document.data != "none"
                else None,
                date=datetime.datetime.now(),
            )
            trial.judgement = judgement
        else:
            trial.judgement.description = form.judgement_description.data
            trial.judgement.judgement = form.judgement.data
            trial.judgement.document_id = (
                form.document.data if form.document.data != "none" else None
            )
        db.session.commit()
        flash("Die Verhandlung wurde erfolgreich bearbeitet.", "success")
        return redirect(url_for("cases.edit_case_trials", case_id=trial.case_id))
    elif request.method == "GET":
        form.name.data = trial.name
        form.date.data = trial.date
        form.description.data = trial.description
        if trial.address is not None:
            form.use_address.data = True
            form.country.data = trial.address.country
            form.city.data = trial.address.city
            form.zip_code.data = trial.address.zip_code
            form.street.data = trial.address.street
            form.house_number.data = trial.address.house_number
        if trial.judgement is not None:
            form.judgement_description.data = trial.judgement.description
            form.judgement.data = trial.judgement.judgement.name
            form.document.data = trial.judgement.document_id

    return render_template(
        "edit_trial.html",
        trial=trial,
        form=form,
    )
