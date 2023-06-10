from app.models.models import CaseStatus
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileField, FileRequired, FileAllowed


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


class AddInvolvedPerson(FlaskForm):
    person = SelectField(
        "Person",
        validators=[DataRequired()],
        choices=[],
        description="Person",
    )
    role = SelectField(
        "Rolle",
        validators=[DataRequired()],
        choices=[],
        description="Rolle",
    )


class UploadDocumentForm(FlaskForm):
    file = FileField(
        "Datei",
        validators=[FileRequired()],
        description="Datei",
    )
    description = StringField(
        "Beschreibung",
        validators=[DataRequired(), Length(min=1, max=50)],
        description="Beschreibung",
    )
