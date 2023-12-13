from flask import request, Response, Blueprint

import controllers

categories = Blueprint("categories", __name__)


@categories.route("/category", methods=["post"])
def category_add() -> Response:
    return controllers.category_add(request)

@categories.route("/categories", methods=["GET"])
def categories_get_all() -> Response:
    return controllers.categories_get_all(request)

@categories.route("/category/<category_id>", methods=["GET"])
def category_get_by_id(category_id) -> Response:
    return controllers.category_get_by_id(request, category_id)
