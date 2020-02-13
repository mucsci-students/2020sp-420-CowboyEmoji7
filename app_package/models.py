"""Contains representations of the data model."""

from app_package import db, ma
from datetime import datetime

class ClassSchema(db.Model):
    """Data model for representation of classes in current diagram.
    
    Use 'name' as primary key because names are unique identifiers
    """

    name = db.Column(db.String(200), primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    x = db.Column(db.Integer())
    y = db.Column(db.Integer())
    
    def __repr__(self):
        return '<Class %r>' % self.name

class SaveSchema(ma.ModelSchema):
    """Meta model used by flask-marshmallow in jsonification."""
    
    class Meta:
        model = ClassSchema