from flask import Blueprint, render_template


services_blueprint = Blueprint('services', __name__, url_prefix='/services')


@services_blueprint.route("/", methods=["GET"])
def services_list():
    return render_template('services/services.html')


@services_blueprint.route("/add", methods=["GET", "POST"])
def services_add():
    pass


@services_blueprint.route("/remove", methods=["POST"])
def remove_service():
    pass
