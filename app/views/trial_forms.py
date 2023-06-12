from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField
from wtforms.validators import DataRequired, Length


class EditTrialForm(FlaskForm):
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
