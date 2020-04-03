"""Useful to clear and remake the database"""

from app_package import db
from app_package.models import Class, ClassSchema, Relationship, Attribute, RelationshipSchema, AttributeSchema

db.drop_all()
db.create_all()