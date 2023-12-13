from flask import request, Response, Blueprint

import controllers

products = Blueprint("products", __name__)


@products.route("/product", methods=["POST"])
def product_add() -> Response:
    return controllers.product_add(request)

@products.route("/products", methods=["GET"])
def products_get_all() -> Response:
    return controllers.products_get_all()