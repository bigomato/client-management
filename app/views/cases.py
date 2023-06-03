from flask import Blueprint, flash, redirect, request, url_for
from flask import render_template
from sqlalchemy import or_
from app import db
from app.models.models import *

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
