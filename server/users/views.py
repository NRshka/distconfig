from typing import Optional
from flask_login import login_user
from flask import flash, abort, request, render_template, redirect, url_for

from server.app import app, users_manager
from .forms import LoginForm, RegisterForm
from .users import User


@app.route("/login", methods=["GET", "POST"])
def authenticate_user():
    form = LoginForm(request.form)
    if request.method == "POST":

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            user: Optional[User] = users_manager.authorize(username, password)

            if user:
                login_user(user)
                return redirect(url_for("index_page"))
            else:
                flash("Username and/or password are not correct")

    return render_template("users/login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register_user():
    form = RegisterForm(request.form)
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            fullname = form.fullname.data

            user: Optional[User] = users_manager.register(username, email, password, fullname)
            # TODO exception handling
            import pdb
            pdb.set_trace()
            login_user(user)
            return redirect(url_for("index_page"))

    return render_template("users/register.html", form=form)


@app.route("/users", methods=["GET"])
def users_list():
    pass


@app.route("/logout", methods=["GET"])
def logout():
    pass


@app.route("/user_profile", methods=["GET"])
def user_profile():
    pass



