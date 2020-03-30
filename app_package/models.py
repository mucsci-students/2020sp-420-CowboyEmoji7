"""Contains representations of the data model."""

from app_package import db, ma
from datetime import datetime
from sqlalchemy.orm import relationship


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

    __relationship__ = 'relationship'
    from_name = db.Column(db.String(200), db.ForeignKey('class.name'), primary_key=True)
    to_name = db.Column(db.String(200), db.ForeignKey('class.name'), primary_key=True)
    rel_type = db.Column(db.String(10)) # agg,comp,gen,none
    parent_class = relationship("Class", back_populates="class_relationships", foreign_keys=[from_name, to_name], primaryjoin='Class.name==Relationship.from_name')
    

class Theme(db.Model):
    __tablename__ = 'theme'
    name = db.Column(db.String(200), primary_key=True)
    active = db.Column(db.Boolean, default=True)
    

class ClassSchema(ma.ModelSchema):
    """Meta model used by flask-marshmallow in jsonification."""
    
    class Meta:
        model = Class

class RelationshipSchema(ma.ModelSchema):
    member_of = ma.Nested(ClassSchema)
    class Meta:
        fields = ("from_name", "to_name", "rel_type")
        model = Relationship

class AttributeSchema(ma.ModelSchema):
    member_of = ma.Nested(ClassSchema)
    class Meta:
        model = Attribute

class ThemeSchema(ma.ModelSchema):
    """Meta model used by flask-marshmallow in jsonification."""
    
    class Meta:
        model = Theme