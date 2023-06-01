from flask import Blueprint, redirect, request, url_for
from flask import render_template
from app import db
from app.models.models import *

cases = Blueprint("cases", __name__)


@cases.route("/cases")
def cases_page():
    page = request.args.get("page", 1, type=int)
    select = db.session.query(Case)
    cases = db.paginate(select, page=page, per_page=16, error_out=False)
    if page > cases.pages:
        return redirect(url_for("cases.cases_page", page=cases.pages))
    return render_template("cases.html", CaseStatus=CaseStatus, cases=cases)
