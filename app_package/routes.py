"""Connects front-end to back-end.

Contains routes through which requests from
  the view are passed to interact with the data model.
"""

from app_package.models import Class, ClassSchema, Relationship, RelationshipSchema, Attribute
from flask import render_template, json, url_for, request, redirect, flash, Response
from app_package import app, db
from app_package.core_func import (core_add, core_delete, core_save, core_update,
                                   core_load, core_add_attr, core_del_attr, 
                                   core_update_attr, core_add_rel, core_del_rel,
                                   core_parse)
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
            if core_add(class_):
                flash('ERROR: Unable to add class ' + class_, 'error')
        return redirect('/')

    else:
        # grab all entries in order
        classes = Class.query.order_by(Class.date_created).all()
        attributes = Attribute.query.order_by(Attribute.date_created).all()
        return render_template('index.html', classes=classes, attributes=attributes)


@app.route('/delete/', methods=['POST'])
def delete():
    """Deals with requests to remove a class.

    Removes the requested class from database, if successful
    """
    try:
        name = request.form['delete']
        if core_delete(name):
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
    updatee.x = x
    updatee.y = y

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
                    addAttributes(class_name, theDict[el]['attrs'])
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
    if core_update(oldName, newName):
        flash("ERROR: Unable to update class " + oldName + " to " + newName, 'error')

def delAttribute(name, attr):
    """Helper to remove attributes from class."""

    if core_del_attr(name, attr):
        flash("ERROR: Unable to remove attribute " + attr + " from " + name, 'error')

def updateAttribute(name, oldAttr, newAttr):
    """Helper to update attributes in class."""

    if core_update_attr(name, oldAttr, newAttr):
        flash("ERROR: Unable to update attribute " + oldAttr + " in " + name + " to " + newAttr, 'error')

def addAttributes(name, attrString):
    """Helper to add attributes to class."""
    attrList = core_parse(attrString)
    for attr in attrList:
        if core_add_attr(name, attr):
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
        if core_add_rel(fro, child):
            flash("ERROR: Unable to add relationship from " + fro + " to " + child, 'error')

def delRelationship(fro, to):
    """Helper function to remove relationships from class."""
    for child in to:
        if core_del_rel(fro, child):
            flash("ERROR: Unable to delete relationship from " + fro + " to " + child, 'error')

@app.route("/getRelationships/", methods=['POST'])
def getRelationship():
    """Helper route to give relationship information to JS."""
    rels = Relationship.query.all()

    rel_schema = RelationshipSchema(many=True)
    out = rel_schema.dump(rels)

    return json.dumps(out)