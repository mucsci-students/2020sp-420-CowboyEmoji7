from app_package import db
from datetime import datetime


class ClassSchema(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    content = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    #x = db.Column(db.String(6))
    #y = db.Column(db.String(6))
    
    def __repr__(self):
        return '<Task %r>' % self.name