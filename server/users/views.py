from typing import Optional
from flask_login import login_user
from flask import flash, abort, request, render_template, redirect, url_for

from server.app import app, users_manager
from .forms import LoginForm
from .users import User


@app.route('/login', methods=['GET', 'POST'])
def authenticate_user():
    form = LoginForm(request.form)
    if request.method == 'POST':

        if form.validate_on_submit():
            username = form.username
            password = form.password


            user: Optional[User] = users_manager.authorize(username, password)

            if user:
                login_user(user)
                return redirect(url_for('index_page'))
            else:
                flash("Username and/or password are not correct")
                abort(403)
    
    return render_template('users/login.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        return render_template('users/login.html', form=form)
