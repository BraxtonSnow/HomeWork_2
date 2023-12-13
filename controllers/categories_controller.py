from flask import Response, jsonify

from db import db 
from util.reflection import populate_object
from models.categories import Categories, category_schema, categories_schema


def category_add(req) -> Response:
    post_data = req.form if req.form else req.json
    new_category = Categories.get_new_category()

    populate_object(new_category, post_data)

    db.session.add(new_category)
    db.session.commit()

    return jsonify(category_schema.dump(new_category)), 201


def categories_get_all(req) -> Response:

    query = db.session.query(Categories).all()

    return jsonify(categories_schema.dump(query)), 200


def category_get_by_id(req, category_id) -> Response:
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    return jsonify(category_schema.dump(query)), 200

