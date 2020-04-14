"""Contains core controller functionality connecting view to data model."""

from app_package.models import Class, ClassSchema, Attribute, AttributeSchema, Relationship, RelationshipSchema
from app_package import app, db
from flask import json

def core_add(class_name):
    """Adds a class with the given name to the database

    Returns 0 on success, 1 on failure
    """
    try:
        if "'" in class_name or '"' in class_name:
            return 1
        new_class = Class(name=class_name, x=0, y=0)
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

        relations = Relationship.query.filter(class_name == Relationship.from_name).all()
        for rel in relations:
            db.session.delete(rel)

        relations = Relationship.query.filter(class_name == Relationship.to_name).all()
        for rel in relations:
            db.session.delete(rel)

        attributes = Attribute.query.filter(class_name == Attribute.class_name).all()
        for attr in attributes:
            db.session.delete(attr)

        db.session.delete(class_to_delete)
        db.session.commit()
        return 0
    except:
        db.session.rollback()
        return 1

def core_update(old_name, new_name):
    """Updates a class with the given name from the database with a new name.

    Returns 0 on success, 1 on failure
    """

    try:
        if "'" in new_name or '"' in new_name:
            return 1
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
        db.session.rollback()
        return 1

def core_save():
    """Creates a string with JSONified data representing the database

    Returns proper string on success, None on failure
    """
    
    classes = Class.query.all()

    # Use flask-marshmallow to "jsonify" current data
    class_schema = ClassSchema(many=True)
    out = class_schema.dump(classes)

    # Options utilized strictly for readability of the resulting file
    return json.dumps(out, ensure_ascii=False, indent=4)

def core_load(data):
    """Populates the database with the contents of passed data array.

    Returns 0 on success, 1 on failure
    """
    try:
        classes = Class.query.all()
        for item in classes:
            db.session.delete(item)
        
        for element in data:
            if "'" in element["name"] or '"' in element["name"]:
                raise ValueError("Double and single quotes are disallowed in class names.")
                return 1
            newClass = Class(
                name=element["name"],
                x=max(element["x"], 0),
                y=max(element["y"], 0)
            )
            db.session.add(newClass)
        db.session.commit()

        for element in data:
            for attr in element["class_attributes"]:
                newAttr = Attribute(
                    attribute=attr["attribute"],
                    class_name=attr["class_name"],
                    attr_type=attr["attr_type"]
                )
                db.session.add(newAttr)


            for rel in element["class_relationships"]:
                newRel = Relationship(
                    from_name=rel["from_name"],
                    to_name=rel["to_name"],
                    rel_type=rel["rel_type"]
                )
                db.session.add(newRel)

        db.session.commit()
        return 0
    except:
        db.session.rollback()
        return 1

def core_add_attr(pName, attr, attrType):
    """Adds an attribute to class with given name in the database

    Returns 0 on success, 1 on failure
    """

    try:
        if Class.query.get(pName) is None:
            return 1
        new_attr = Attribute(attribute=attr, class_name=pName, attr_type=attrType)
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
        attr_to_delete = Attribute.query.get({"class_name": pName, "attribute": attr})
        if (attr_to_delete is None):
            return 1

        db.session.delete(attr_to_delete)
        db.session.commit()
        return 0
    except:
        db.session.rollback()
        return 1

def core_update_attr(pName, attr, newAttr):
    """Updates an attribute in class with given name in the database

    Returns 0 on success, 1 on failure
    """

    try:
        attr_to_update = Attribute.query.get({"class_name": pName, "attribute": attr})
        if (attr_to_update is None):
            return 1

        attr_to_update.attribute = newAttr
        db.session.commit()
        
        parsedType = parseType(newAttr)
        if parsedType is not None:
            # link it to the related class if applicable
            ClassList = Class.query.all()
            for CurrentClass in ClassList:
                if CurrentClass.name == parsedType:
                    core_add_rel(pName, CurrentClass.name, "agg")
                    break
                
        return 0
    except:
        db.session.rollback()
        return 1

def core_add_rel(from_name, to_name, rel_type):
    """Adds a relationship to class with given name in the database

    Returns 0 on success, 1 on failure
    """

    try:
        if (Class.query.get(from_name) is None or Class.query.get(to_name) is None):
            return 1
        new_rel = Relationship(from_name=from_name, to_name=to_name, rel_type=rel_type)
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
        rel_to_delete = Relationship.query.get({"from_name": from_name, "to_name": to_name})
        if (rel_to_delete is None):
            return 1
        
        db.session.delete(rel_to_delete)
        db.session.commit()
        return 0
    except:
        db.session.rollback()
        return 1

def core_parse (string):
    """Parses useful tokens for data manipulation from a string list with comma delimiters"""
    parensUnmatched = 0
    stringBuf = ""
    listBuf = []

    for el in string:
        if el == '(':
            parensUnmatched += 1
        elif el == ')' and parensUnmatched > 0:
            parensUnmatched -= 1
        elif el == ',' and parensUnmatched == 0:
            if stringBuf != "":
                stringBuf = removeTrailingWhitespace(stringBuf)
                listBuf.append(stringBuf)
                stringBuf = ""
                
            continue
        if not ((el == ' ' or el == '\t') and stringBuf == ""):
            stringBuf += el

    if stringBuf != "": 
        stringBuf = removeTrailingWhitespace(stringBuf)
        listBuf.append(stringBuf)
        
    return listBuf

def removeTrailingWhitespace(string):
    """Helper function which removes trailing whitespace from a string"""
    while (string[-1] == ' ' or string[-1] == '\t'):
        string = string[0:-1]
    return string

def parseType(input):
    """Parses type from a string attribute in the following formats:
      <type> <name>
      <name>:<type>"""
    # remove the crap in parens
    front = input.split('(', 1)[0]
    tipe = ""
    try:
        # if it uses a colon
        tipe = front.split(':',1)[1]
    except:
        # if it doesn't use a colon
        tipe = front.split(' ')[0]
    # if it doesn't have a type
    if tipe == front:
        tipe = None
    return(tipe)

def core_clear():
    """Clears all existing classes from the database."""
    db.drop_all()
    db.create_all()