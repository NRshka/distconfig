from flask import Blueprint


configs_blueprint = Blueprint('configs', __name__, url_prefix='/configs')


@configs_blueprint.route("/", methods=["GEt"])
def configs_list():
    pass
