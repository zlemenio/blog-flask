from flask_wtf import Form
from wtforms.csrf.session import SessionCSRF
from wtforms import validators, ValidationError
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, EqualTo


class MyBaseForm(Form):
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b'EPejf00jpfj8Gx1SjnyLxwBEDQfnQ9DJYe0Ym'


class AddTask(MyBaseForm):
    category = StringField("Category", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    submit = SubmitField("Save")


class EditTask(MyBaseForm):
    category = StringField("Category", validators=[DataRequired()])
    description = TextAreaField("Description", validators=[DataRequired()])
    status = SelectField("Status", choices=['Pending', 'Done'])
    submit = SubmitField("Save")


class DeleteTask(MyBaseForm):
    delete_task_id = HiddenField()
    submit = SubmitField("Delete")
