from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField
from wtforms.validators import DataRequired, Email, Length


class CreateClientForm(FlaskForm):
    name = StringField(
        "Vorname",
        validators=[DataRequired(), Length(min=1, max=50)],
        description="Vorname",
    )
    surname = StringField(
        "Nachname",
        validators=[DataRequired(), Length(min=1, max=50)],
        description="Nachname",
    )
    birthdate = DateField("Geburtstag", validators=[DataRequired()])
    phone_number = StringField(
        "Telefonnummer",
        validators=[DataRequired(), Length(min=7, max=50)],
        description="Telefonnummer",
    )
    email = EmailField(
        "E-mail",
        validators=[DataRequired(), Email(), Length(min=1, max=50)],
        description="E-mail Addresse",
    )
    country = StringField("Land", validators=[DataRequired()], description="Land")
    city = StringField("Stadt", validators=[DataRequired()], description="Stadt")
    zip_code = StringField(
        "Postleitzahl", validators=[DataRequired()], description="Postleitzahl"
    )
    street = StringField("Straße", description="Straße")
    house_number = StringField("Hausnummer", description="Hasunummer")
