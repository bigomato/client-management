from flask import Blueprint, redirect, request, url_for
from flask import render_template
from app import db
from app.models.models import *

lawyers = Blueprint("lawyers", __name__)


@lawyers.route("/lawyers")
def lawyers_page():
    page = request.args.get("page", 1, type=int)
    select = db.session.query(Person).filter(Person.our_lawyer == True)
    lawyers = db.paginate(select, page=page, per_page=16, error_out=False)
    if page > lawyers.pages:
        return redirect(url_for("lawyers.lawyers_page", page=lawyers.pages))
    return render_template("lawyers.html", lawyers=lawyers)
