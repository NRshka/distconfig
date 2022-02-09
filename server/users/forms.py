from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = TextField("Login", validators=[DataRequired(), Length(min=6, max=20)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=48)])


class RegisterForm(FlaskForm):
    username = TextField("Login", validators=[DataRequired(), Length(min=6, max=20)])
    email = TextField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=48)]
    )
    confirm = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    fullname = TextField("Full Name", validators=[DataRequired()])
