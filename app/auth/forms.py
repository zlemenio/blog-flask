
from flask_wtf import Form
from wtforms.csrf.session import SessionCSRF
from wtforms import validators, ValidationError
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, EqualTo


class MyBaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b'EPejf00jpfj8Gx1SjnyLxwBEDQfnQ9DJYe0Ym'


class Login(MyBaseForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember?")
    submit = SubmitField("Log in")


class Register(MyBaseForm):
    email = StringField("Email", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    passConfirm = PasswordField(
        "Password confirm", validators=[
            DataRequired()])
    submit = SubmitField("Sign up")
