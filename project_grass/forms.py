from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=100)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6)]
    )


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=100)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6)]
    )
