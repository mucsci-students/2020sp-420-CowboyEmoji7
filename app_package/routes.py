"""Connects front-end to back-end.

Contains routes through which requests from
  the view are passed to interact with the data model.
"""

from app_package.models import Class, ClassSchema, Relationship, RelationshipSchema, Attribute
from flask import render_template, json, url_for, request, redirect, flash, Response
from app_package import app, db, cmd_stack
from app_package.core_func import core_save, core_load, core_parse
from app_package.memento.func_objs import (add_class, delete_class, edit_class, 
                                           add_attr, del_attr, edit_attr, add_rel,
                                           del_rel, move)


@app.route('/', methods=['POST', 'GET'])
def index():
    """Deals with requests to the base index.

    On POST request, adds requested class and redirects
      to itself to re-render with updated data
    On GET request, renders the base index with current data
    """

    if request.method == 'POST':
        # form tag 'content'
        class_name = request.form['class_name']

        if class_name == '':
            return redirect('/')

        classList = core_parse(class_name)
        for class_ in classList:
            addCmd = add_class(class_)
            if cmd_stack.execute(addCmd):
                flash('ERROR: Unable to add class ' + class_, 'error')
        return redirect('/')

    else:
        # grab all entries in order
        classes = Class.query.order_by(Class.date_created).all()
        attributes = Attribute.query.order_by(Attribute.date_created).all()
        return render_template('index.html', classes=classes, attributes=attributes, cmd_stack=cmd_stack)


@app.route('/addAttribute/', methods=['POST'])
def add_attribute():
    """Deals with requests to add an attribute to a class.
    
    Adds the requested attribute to the database, if successful
    """
    name = request.form['class_name']
    attrName = request.form['attribute']
    attrList = core_parse(attrName)
    for attr in attrList:
        addAttrCmd = add_attr(name, attr)
        if cmd_stack.execute(addAttrCmd):
            flash('ERROR: Unable to add attribute ' + attr + " to " + name, 'error')
    return redirect('/')


@app.route('/delete/', methods=['POST'])
def delete():
    """Deals with requests to remove a class.

    Removes the requested class from database, if successful
    """
    try:
        name = request.form['delete']
        deleteCmd = delete_class(name)
        if cmd_stack.execute(deleteCmd):
            flash('ERROR: Unable to delete class ' + name, 'error')
    except:
        flash("Invalid name", 'error')

    return redirect('/')


@app.route('/update/', methods=['POST'])
def update():
    """Deals with requests to update a class.

    Edits the requested class in database, if successful
    """
    try:
        oldName = request.form['old_name']
        newName = request.form['new_name']
        editCmd = edit_class(oldName, newName)
        if cmd_stack.execute(editCmd):
            flash("ERROR: Unable to update class " + oldName + " to " + newName, 'error')
    except:
        flash("Invalid arguments, try again.", 'error')
    
    return redirect('/')


@app.route('/save/', methods=['POST'])
def save():
    """Deals with requests to save current data locally.

    JSONify current data and return the result in a .json file
      as an attachment--to download--with requested name
    """
    try:
        name = request.form['save_name']
        contents = core_save()
        return Response(contents, mimetype="application/json", headers={"Content-disposition": "attachment; filename=" + name + ".json;"})
    except:
        flash("There was a problem saving. Try again.", 'error')
        return redirect('/')


@app.route("/load/", methods=['POST'])
def load():
    """Deals with requests to load pre-existing user data from a user's storage.

    Clears current data, then loads file given by user
    Then, adds each datum to the working database and
      redirects to base index to re-render with loaded data
    """

    try:
        Jfile = request.files['file']
        if core_load(json.load(Jfile)):
            flash("ERROR: Unable to load data into database", 'error')
    except:
        flash("Invalid JSON", 'error')

    return redirect('/')


@app.route("/updateCoords/", methods=['POST'])
def updateCoords():
    """Deals with requests from GUI to save dragged coordinates."""

    name = request.form['name']
    x = request.form['left']
    y = request.form['top']

    updatee = Class.query.get_or_404(name)
    moveCmd = move(name,  x, y)
    cmd_stack.execute(moveCmd)

    db.session.commit()
    return "Name: " + updatee.name + "\nX: " + str(updatee.x) + "\nY: " + str(updatee.y)


@app.route("/manipAttribute/", methods=['POST'])
def manipAttribute():
    """Deals with requests from GUI to manipulate attributes within a class.
    
    Delegates to helper functions
    """
    try:
        class_name = request.form['class_name']
        attribute = request.form['attribute']
        action = request.form['action']
        if (action == 'Delete'):
            delAttribute(class_name, attribute)
        elif (action == 'Rename'):
            updateAttribute(class_name, attribute, request.form['new_attribute'])
    except:
        flash("Invalid arguments, try again", 'error')
    
    return redirect('/')


def delAttribute(name, attr):
    """Helper to remove attributes from class."""

    delAttrCmd = del_attr(name, attr)
    if cmd_stack.execute(delAttrCmd):
        flash("ERROR: Unable to remove attribute " + attr + " from " + name, 'error')


def updateAttribute(name, oldAttr, newAttr):
    """Helper to update attributes in class."""

    editAttrCmd = edit_attr(name, oldAttr, newAttr)
    if cmd_stack.execute(editAttrCmd):
        flash("ERROR: Unable to update attribute " + oldAttr + " in " + name + " to " + newAttr, 'error')


@app.route("/manipRelationship/", methods=['POST'])
def manipRelationship():
    """Deals with requests from GUI to manipulate relationships.
    
    Delegates to helper functions
    """
    try:
        fro = request.form['class_name']
        to = request.form.getlist('relationship')
        action = request.form['action']
        if (action == 'delete'):
            delRelationship(fro, to)
        elif (action == 'add'):
            addRelationship(fro, to)
    except:
        flash("Invalid arguments, try again.", 'error')
    
    return redirect('/')


def addRelationship(fro, to):
    """Helper function to add relationships to class."""
    for child in to:
        addRelCmd = add_rel(fro, child)
        if cmd_stack.execute(addRelCmd):
            flash("ERROR: Unable to add relationship from " + fro + " to " + child, 'error')


def delRelationship(fro, to):
    """Helper function to remove relationships from class."""
    for child in to:
        delRelCmd = del_rel(fro, child)
        if cmd_stack.execute(delRelCmd):
            flash("ERROR: Unable to delete relationship from " + fro + " to " + child, 'error')


@app.route("/getRelationships/", methods=['POST'])
def getRelationship():
    """Helper route to give relationship information to JS."""
    rels = Relationship.query.all()

    rel_schema = RelationshipSchema(many=True)
    out = rel_schema.dump(rels)

    return json.dumps(out)


@app.route("/undo/", methods=['POST'])
def undo():
    cmd_stack.undo()
    return redirect('/')


@app.route("/redo/", methods=['POST'])
def redo():
    cmd_stack.redo()
    return redirect('/')
