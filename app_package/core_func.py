"""Contains core controller functionality connecting view to data model."""

from app_package.models import Class, ClassSchema, Attribute, AttributeSchema, Relationship, RelationshipSchema
from app_package import app, db
from flask import json

def core_add(class_name):
    """Adds a class with the given name to the database

    Returns 0 on success, 1 on failure
    """
    try:
        new_class = Class(name=class_name)
        db.session.add(new_class)
        db.session.commit()
        return 0
    except:
        db.session.rollback()
        return 1

def core_delete(class_name):
    """Deletes a class with the given name from the database

    Returns 0 on success, 1 on failure
    """
    try:
        class_to_delete = Class.query.get(class_name)
        if (class_to_delete is None):
            return 1

        db.session.delete(class_to_delete)
        db.session.commit()
        return 0
    except:
        return 1

def core_update(old_name, new_name):
    """Updates a class with the given name from the database with a new name.

    Returns 0 on success, 1 on failure
    """

    try:
        class_to_update = Class.query.get(old_name)
        if (class_to_update is None):
            return 1

        relations = Relationship.query.filter(old_name == Relationship.from_name).all()
        for rel in relations:
            rel.from_name = new_name

        relations = Relationship.query.filter(old_name == Relationship.to_name).all()
        for rel in relations:
            rel.to_name = new_name

        attributes = Attribute.query.filter(old_name == Attribute.class_name).all()
        for attr in attributes:
            attr.class_name = new_name

        class_to_update.name = new_name

        db.session.commit()
        return 0

    except:
        return 1

def core_save():
    """Creates a string with JSONified data representing the database

    Returns proper string on success, None on failure
    """
    try:
        classes = Class.query.all()

        # Use flask-marshmallow to "jsonify" current data
        class_schema = ClassSchema(many=True)
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
        classes = Class.query.all()
        for item in classes:
            db.session.delete(item)
        
        for element in data:
            newClass = Class(
                name=element["name"],
                x=element["x"],
                y=element["y"]
            )
            db.session.add(newClass)
        db.session.commit()

        for element in data:
            for attr in element["class_attributes"]:
                newAttr = Attribute(
                    attribute=attr["attribute"],
                    class_name=attr["class_name"]
                )
                db.session.add(newAttr)


            for rel in element["class_relationships"]:
                newRel = Relationship(
                    from_name=rel["from_name"],
                    to_name=rel["to_name"]
                )
                db.session.add(newRel)

        db.session.commit()
        return 0
    except:
        return 1

def core_add_attr(pName, attr):
    """Adds an attribute to class with given name in the database

    Returns 0 on success, 1 on failure
    """

    try:
        new_attr = Attribute(attribute=attr, class_name=pName)
        db.session.add(new_attr)
        db.session.commit()
        return 0
    except:
        db.session.rollback()
        return 1

def core_del_attr(pName, attr):
    """Deletes an attribute from class with given name in the database

    Returns 0 on success, 1 on failure
    """

    try:
        attr_to_delete = Attribute.query.filter(and_(pName == Attribute.class_name, attr == Attribute.attribute))
        if (attr_to_delete is None):
            return 1

        db.session.delete(attr_to_delete)
        db.session.commit()
        return 0
    except:
        return 1

def core_update_attr(pName, attr, newAttr):
    """Updates an attribute in class with given name in the database

    Returns 0 on success, 1 on failure
    """

    try:
        attr_to_update = Attribute.query.filter(and_(pName == Attribute.class_name, attr == Attribute.attribute))
        if (attr_to_update is None):
            return 1

        attr_to_update.attribute = newAttr
        db.session.commit()
        return 0
    except:
        return 1

def core_add_rel(from_name, to_name):
    """Adds a relationship to class with given name in the database

    Returns 0 on success, 1 on failure
    """

    try:
        new_rel = Relationship(from_name=from_name, to_name=to_name)
        db.session.add(new_rel)
        db.session.commit()
        return 0
    except:
        db.session.rollback()
        return 1

def core_del_rel(from_name, to_name):
    """Deletes a relationship from class with given target in the database

    Returns 0 on success, 1 on failure
    """

    try:
        rel_to_delete = Relationship.query.filter(and_(from_name == Relationship.from_name, to_name == Relationship.to_name))
        if (rel_to_delete is None):
            return 1

        db.session.delete(rel_to_delete)
        db.session.commit()
        return 0
    except:
        return 1