from app_package import db, ma
from datetime import datetime


class ClassSchema(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    content = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    x = db.Column(db.Integer())
    y = db.Column(db.Integer())
    
    def __repr__(self):
        return '<Class %r>' % self.name


class SaveSchema(ma.ModelSchema):
    class Meta:
        model = ClassSchema