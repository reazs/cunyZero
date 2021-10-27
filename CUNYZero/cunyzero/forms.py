from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditor, CKEditorField
from cunyzero import app



class StudentRegister(FlaskForm):
    f_name = StringField("First name", validators=[DataRequired()])
    l_name = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    gpa = IntegerField("GPA", validators=[DataRequired()])
    content = CKEditorField("Tell us about yourself", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class StaffRegister(FlaskForm):
    f_name = StringField("First name", validators=[DataRequired()])
    l_name = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    content = CKEditorField("Tell us about yourself")
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    f_email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")