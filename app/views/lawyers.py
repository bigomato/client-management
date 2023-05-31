from flask import Blueprint
from flask import render_template
from app import db
from app.models.models import *

lawyers = Blueprint("lawyers", __name__)


@lawyers.route("/lawyers")
def lawyers_page():
    lawyers = db.session.query(Person).filter(Person.our_lawyer == True).limit(16)
    return render_template("lawyers.html", lawyers=lawyers)
