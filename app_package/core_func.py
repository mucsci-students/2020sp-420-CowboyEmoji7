"""Contains core controller functionality connecting view to data model."""

from app_package.models import ClassSchema, SaveSchema
from app_package import app, db
from flask import json
import datetime

def core_add(class_name):
    """Adds a class with the given name to the database

    Returns 0 on success, 1 on failure
    """
    try:
        new_class = ClassSchema(name=class_name, date_created=datetime.utcnow())
        db.session.add(new_class)
        db.session.commit()
        return 0
    except:
        return 1

def core_delete(class_name):
    """Deletes a class with the given name from the database

    Returns 0 on success, 1 on failure
    """
    try:
        class_to_delete = ClassSchema.query.get(class_name)
        if class_to_delete is None:
            return 1

        db.session.delete(class_to_delete)
        db.session.commit()
        return 0
    except:
        return 1

def core_save():
    """Creates a string with JSONified data representing the database

    Returns proper string on success, None on failure
    """
    try:
        classes = ClassSchema.query.all()

        # Use flask-marshmallow to "jsonify" current data
        class_schema = SaveSchema(many=True)
        out = class_schema.dump(classes)

        # Options utilized strictly for readability of the resulting file
        return json.dumps(out, ensure_ascii=False, indent=4)
    except:
        return None

def core_load(data):
    """Populates the database with the contents of passed data array.

    Returns 0 on success, 1 on failure
    """
    try:
        classes = ClassSchema.query.all()
        for item in classes:
            db.session.delete(item)
        
        for element in data:
            newClass = ClassSchema(
                name=element["name"],
                x=element["x"],
                y=element["y"]
            )
            db.session.add(newClass)

        db.session.commit()
        return 0
    except:
        return 1