"""Contains representations of the data model."""

from app_package import db, ma
from datetime import datetime
from sqlalchemy.orm import relationship
from marshmallow import INCLUDE, fields, Schema


class Class(db.Model):
    """Data model for representation of classes in current diagram.
    
    Use 'name' as primary key because names are unique identifiers
    """

    __tablename__ = 'class'
    name = db.Column(db.String(200), primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    x = db.Column(db.Integer())
    y = db.Column(db.Integer())
    class_attributes = relationship("Attribute", back_populates="parent_class", primaryjoin='Class.name==Attribute.class_name', cascade='all,delete-orphan')
    class_relationships = relationship("Relationship", back_populates="parent_class", primaryjoin='Class.name==Relationship.from_name', cascade='all,delete-orphan')

class Attribute(db.Model):
    """Data model for representation of attributes in current diagram.

    Use 'name'/'parent_name' composite as primary key because this combo is unique
    """

    __tablename__ = 'attribute'
    attribute = db.Column(db.String(200), primary_key=True)
    attr_type = db.Column(db.String(10)) #field, method
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    class_name = db.Column(db.String(200), db.ForeignKey('class.name'), primary_key=True)
    parent_class = relationship("Class", back_populates="class_attributes", foreign_keys=[class_name], primaryjoin='Class.name==Attribute.class_name')

class Relationship(db.Model):
    """Data model for representation of relationships in current diagram.

    Use names 'from'/'to' as composite primary key because this combo is unique
    """

    __tablename__ = 'relationship'
    from_name = db.Column(db.String(200), db.ForeignKey('class.name'), primary_key=True)
    to_name = db.Column(db.String(200), db.ForeignKey('class.name'), primary_key=True)
    rel_type = db.Column(db.String(10)) # agg,comp,gen,none
    parent_class = relationship("Class", back_populates="class_relationships", foreign_keys=[from_name, to_name], primaryjoin='Class.name==Relationship.from_name')
    
    __mapper_args__ = {
        'confirm_deleted_rows': False
    }

class Settings(db.Model):
    """Saves user settings. Currently only saves theme."""

    name = db.Column(db.String(30), primary_key=True)
    value = db.Column(db.String(50))


class RelationshipSchema(Schema):
    """Meta model used by flask-marshmallow in jsonification."""
    from_name = fields.String()
    to_name = fields.String()
    rel_type = fields.String()

class AttributeSchema(Schema):
    """Meta model used by flask-marshmallow in jsonification."""
    attribute = fields.String()
    attr_type = fields.String()
    date_created = fields.DateTime()
    class_name = fields.String()

class ClassSchema(Schema):
    """Meta model used by flask-marshmallow in jsonification."""
    name = fields.String()
    date_created = fields.DateTime()
    x = fields.Int()
    y = fields.Int()
    class_attributes = fields.Nested(AttributeSchema, many=True)
    class_relationships = fields.Nested(RelationshipSchema, many=True)
