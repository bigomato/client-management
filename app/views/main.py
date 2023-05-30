from flask import Blueprint
from flask import render_template
from app import db
from app.models.models import *

main = Blueprint("main", __name__)


@main.route("/")
def start_page():
    clients = db.session.query(Person).filter(Person.our_client == True).count()
    lawyers = db.session.query(Person).filter(Person.our_lawyer == True).count()
    cases = db.session.query(Case).count()
    cases_won = (
        db.session.query(Case).filter(Case.case_status == CaseStatus.won).count()
    )
    cases_lost = (
        db.session.query(Case).filter(Case.case_status == CaseStatus.won).count()
    )
    return render_template(
        "index.html",
        clients=clients,
        lawyers=lawyers,
        cases=cases,
        cases_won=cases_won,
        cases_lost=cases_lost,
    )
