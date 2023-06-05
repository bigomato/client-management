from flask_wtf import FlaskForm
from wtforms import StringField, DateField, EmailField
from wtforms.validators import DataRequired, Email, Length


class CreateClientForm(FlaskForm):
    name = StringField("name", validators=[DataRequired(), Length(min=1, max=50)])
    surname = StringField("surname", validators=[DataRequired(), Length(min=1, max=50)])
    birthdate = DateField("birthdate", validators=[DataRequired()])
    phone_number = StringField(
        "phone_number", validators=[DataRequired(), Length(min=7, max=50)]
    )
    email = EmailField(
        "email", validators=[DataRequired(), Email(), Length(min=1, max=50)]
    )
    country = StringField("country", validators=[DataRequired()])
    city = StringField("city", validators=[DataRequired()])
    zip_code = StringField("zip_code", validators=[DataRequired()])
    street = StringField("street")
    house_number = StringField("house_number")
