from flask import Blueprint, flash, redirect, request, url_for
from flask import render_template
from sqlalchemy import or_
from app import db
from app.models.models import *
from sqlalchemy import func

lawyers = Blueprint("lawyers", __name__)

func.l


@lawyers.route("/lawyers")
def lawyers_page():
    page = request.args.get("page", 1, type=int)
    search = request.args.get("search", "", type=str)
    select = db.session.query(Person).filter(Person.our_lawyer == True)
    if search != "":
        select = select.filter(
            or_(
                Person.name.like(f"%{search}%"),
                Person.surname.like(f"%{search}%"),
                Person.birthdate.like(f"%{search}%"),
            )
        )
    lawyers = db.paginate(select, page=page, per_page=16, error_out=False)
    if search != "" and lawyers.total == 0:
        flash(
            "Es wurden keine Anwälte, die auf Ihre Suche passen, gefunden.", "warning"
        )
        return redirect(url_for("lawyers.lawyers_page", page=1, s=""))
    if page > lawyers.pages:
        return redirect(url_for("lawyers.lawyers_page", page=lawyers.pages, s=search))
    return render_template("lawyers.html", lawyers=lawyers, search=search)
