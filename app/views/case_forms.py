from app.models.models import CaseStatus
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, DateField
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


class CreateCaseForm(FlaskForm):
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


class CreateTrialForm(FlaskForm):
    # name, date, description
    name = StringField(
        "Name",
        validators=[DataRequired(), Length(min=1, max=50)],
        description="Name",
    )
    date = DateField(
        "Datum",
        validators=[DataRequired()],
        description="Datum",
    )
    description = StringField(
        "Beschreibung",
        validators=[DataRequired(), Length(min=1, max=50)],
        description="Beschreibung",
    )
    use_address = BooleanField(
        "Adresse verwenden",
        validators=[],
        description="Adresse verwenden",
    )
    country = StringField("Land", description="Land")
    city = StringField("Stadt", description="Stadt")
    zip_code = StringField("Postleitzahl", description="Postleitzahl")
    street = StringField("Straße", description="Straße")
    house_number = StringField("Hausnummer", description="Hasunummer")


class AddAttendeeForm(FlaskForm):
    pass
