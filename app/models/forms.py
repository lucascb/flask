from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email


class RegisterForm(Form):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    email = StringField("email", validators=[Email()])
    name = StringField("name", validators=[DataRequired()])


class LoginForm(Form):
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")


class TwitForm(Form):
    content = TextAreaField("content", validators=[DataRequired()])
