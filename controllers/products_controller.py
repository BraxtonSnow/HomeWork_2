from flask import jsonify, Response

from db import db 
from util.reflection import populate_object
from models.products import Products, product_schema, products_schema


def product_add(req) -> Response:
    post_data = req.form if req.form else req.json
    new_product = Products.get_new_product()

    populate_object(new_product, post_data)

    db.session.add(new_product)
    db.session.commit()

    return jsonify(product_schema.dump(new_product)), 201


def products_get_all(req) -> Response:
    query = db.session.query(Products).all()

    return jsonify(products_schema.dump(query)), 200