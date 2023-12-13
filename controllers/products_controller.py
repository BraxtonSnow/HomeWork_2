from flask import jsonify, Response

from db import db 
from util.reflection import populate_object
from models.products import Products, product_schema, products_schema
from models.categories import Categories, categories_schema, category_schema


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


def product_get_by_id(req, product_id) -> Response:
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    return jsonify(product_schema.dump(query)), 200


def product_update_by_id(req, product_id) -> Response:
    post_data = req.form if req.form else req.json

    query = db.session.query(Products).filter(Products.product_id == product_id).first()

    if query:

        populate_object(query, post_data)

    
    try:

        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("ERROR: unable to update record"), 400
    
    return jsonify({"message": "Record updated successfully", "product": product_schema.dump(query)}), 200


def product_activity(req, product_id) -> Response:
    query = db.session.query(Products).filter(Products.product_id == product_id).first()

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



def product_delete_by_id(req, product_id) -> Response:
    product_query = db.session.query(Categories).filter(Products.product_id == product_id).first()

    try:

        db.session.delete(product_query)
        db.session.commit()

    except:

        db.session.rollback()

        return jsonify("ERROR: unable to delete product")
    
    return jsonify(f"Product with product_id {product_id} deleted"), 200




def product_add_category(req) -> Response:
    post_data = req.form if req.form else req.json
    product_id = post_data.get("product_id")
    category_id = post_data.get("category_id")

    product_query = db.session.query(Products).filter(Products.product_id == product_id).first()
    category_query = db.session.query(Categories).filter(Categories.category_id == category_id).first()

    product_query.categories.append(category_query)
    db.session.commit()

    return jsonify({"message": "Category added", "product": product_schema.dump(product_query)}), 200

