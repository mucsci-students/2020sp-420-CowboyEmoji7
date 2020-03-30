"""Connects front-end to back-end.

Contains routes through which requests from
  the view are passed to interact with the data model.
"""

from app_package.models import Class, ClassSchema, Relationship, RelationshipSchema, Attribute, Theme
from flask import render_template, json, url_for, request, redirect, flash, Response
from app_package import app, db, cmd_stack
from app_package.core_func import core_save, core_load, core_parse
from app_package.memento.func_objs import (add_class, delete_class, edit_class, 
                                           add_attr, del_attr, edit_attr, add_rel,
                                           del_rel, move)
from parse import *


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
        themes = Theme.query.all()
        activeTheme = Theme.query.filter(Theme.active == True).first()
        return render_template('index.html', classes=classes, attributes=attributes, cmd_stack=cmd_stack, themes=themes, activeTheme=activeTheme)


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

@app.route("/manipCharacteristics/", methods=['POST'])
def manipCharacteristics():
    """Deals with requests from GUI to manipulate characteristics of a class.
    
    Delegates to helper functions
    """

    try:
        theDict = {}
        for key, value in request.form.to_dict().items():
            field = parse ("field[{}][{}]", key)
            theDict.setdefault(field[0], {}).update({field[1]: value})

        class_name = theDict[' super ']['class_name']
        for el in theDict:
            if 'action' not in theDict[el]:
                if theDict[el]['new_attribute'] != theDict[el]['attribute']:
                    #rename
                    if theDict[el]['new_attribute'] != "":
                        updateAttribute(class_name, theDict[el]['attribute'], theDict[el]['new_attribute'])
            else:
                action = theDict[el]['action']

                if action == "Add":
                    if 'attr_type' in theDict[el]:
                        addAttributes(class_name, theDict[el]['attrs'], theDict[el]['attr_type'])
                elif action == "Delete":
                    delAttribute(class_name, theDict[el]['attribute'])
                elif action == "RenameClass":
                    update(class_name, theDict[el]['new_name'])
                    class_name = theDict[el]['new_name']

    except:
        flash("Invalid arguments, try again", 'error')
    
    return redirect('/')

def update(oldName, newName):
    """Helper to update a class's name."""
    updateCmd = edit_class(oldName, newName)
    if cmd_stack.execute(updateCmd):
        flash("ERROR: Unable to update class " + oldName + " to " + newName, 'error')

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

def addAttributes(name, attrString, attrType):
    """Helper to add attributes to class."""
    attrList = core_parse(attrString)
    for attr in attrList:
        addAttrCmd = add_attr(name, attr, attrType)
        if cmd_stack.execute(addAttrCmd):
            flash('ERROR: Unable to add attribute ' + attr + " to " + name, 'error')


@app.route("/manipRelationship/", methods=['POST'])
def manipRelationship():
    """Deals with requests from GUI to manipulate relationships.
    
    Delegates to helper functions
    """
    try:
        fro = request.form['class_name']
        to = request.form.getlist('relationship')
        action = request.form['action']
        rel_type = request.form['rel_type']
        if (action == 'delete'):
            delRelationship(fro, to)
        elif (action == 'add'):
            addRelationship(fro, to, rel_type)
    except:
        flash("Invalid arguments, try again.", 'error')
    
    return redirect('/')


def addRelationship(fro, to, rel_type):
    """Helper function to add relationships to class."""
    for child in to:
        addRelCmd = add_rel(fro, child, rel_type)
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


@app.route("/updateTheme/", methods=['POST', 'GET'])
def updateTheme():
    oldTheme = Theme.query.filter(Theme.active == True).all()
    newTheme = Theme.query.get({"name": request.form['theme']})

    for theme in oldTheme:
        theme.active = False

    newTheme.active = True
    db.session.commit()
    return redirect('/')


@app.route("/undo/", methods=['POST'])
def undo():
    cmd_stack.undo()
    return redirect('/')


@app.route("/redo/", methods=['POST'])
def redo():
    cmd_stack.redo()
    return redirect('/')
