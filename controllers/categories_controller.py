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


def category_update_by_id(req, category_id) -> Response:
    post_data = req.form if req.form else req.json

    query =  db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if query:

        populate_object(query, post_data)

        try:

            db.session.commit()

        except:

            db.session.rollback()

            return jsonify("ERROR: could not update.")

        return jsonify(category_schema.dump(query)), 200
    
    else:

        return jsonify(f" Category with category_id  {category_id} not found"), 404


def category_activity(req, category_id) -> Response:
    query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    if query:
        query.active = not query.active

        try:

            db.session.commit()

            if query.active:

                return jsonify("record activated successfully"), 200
            
            else:

                return jsonify("record deactivated successfully"), 200

        except:

            db.session.rollback()

            if query.active:

                return jsonify("record not activated successfully"), 400
            
            else:

                return jsonify("record not deactivated successfully"), 400
            
    else:

        return jsonify(f"product with product_id {product_id} not found"), 404


def category_delete_by_id(req, category_id) -> Response:
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    try:

        db.session.delete(category_query)
        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("ERROR: unable to delete category")
    
    return jsonify(f"Category with category_id {category_id} deleted"), 200