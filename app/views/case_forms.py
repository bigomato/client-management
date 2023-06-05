from app.models.models import CaseStatus
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email, Length


class EditCaseFrom(FlaskForm):
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=1, max=50)],
        description="Name",
    )
    description = StringField(
        "Beschreibung",
        validators=[DataRequired(), Length(min=1, max=50)],
        description="Beschreibung",
    )
    case_status = SelectField(
        "Status",
        validators=[DataRequired()],
        choices=[(status.name, status.display()) for status in CaseStatus],
        description="Status",
    )
