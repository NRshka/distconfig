from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = TextField("Login", validators=[DataRequired(), Length(min=6, max=20)])
    password = TextField("Password", validators=[DataRequired(), Length(min=6, max=48)])
