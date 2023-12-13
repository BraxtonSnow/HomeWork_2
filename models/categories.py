import uuid
from sqlalchemy.dialects.postgresql import UUID
import marshmallow as ma

from db import db 

class Categories(db.Model):
    __tablename__= "Categories"

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = db.Column(db.String(), unique=True, nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)


    def __init__(self, category_name, active):
        self.category_name = category_name
        self.active = active

    
    def get_new_category():
        return Categories("", True)


class CategoriesSchema(ma.Schema):
    class Meta:
        fields = ["category_id", "category_name", "active"]

category_schema = CategoriesSchema()
categories_schema = CategoriesSchema(many=True)