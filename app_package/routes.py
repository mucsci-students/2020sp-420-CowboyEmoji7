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


@app.route('/addAttribute/', methods=['POST'])
def add_attr():
    """Deals with requests to add an attribute to a class.
    
    Adds the requested attribute to the database, if successful
    """
    name = request.form['class_name']
    attrName = request.form['attribute']
    attrList = core_parse(attrName)
    for attr in attrList:
        if core_add_attr(name, attr):
            flash('ERROR: Unable to add attribute ' + attr + " to " + name, 'error')
    return redirect('/')


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

@app.route('/update/', methods=['POST'])
def update():
    """Deals with requests to update a class.

    Edits the requested class in database, if successful
    """
    try:
        oldName = request.form['old_name']
        newName = request.form['new_name']
        if core_update(oldName, newName):
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
        if contents is None:
            flash("There was a problem saving. Try again.", 'error')
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
    try:
        name = request.form['name']
        x = request.form['left']
        y = request.form['top']

        updatee = Class.query.get_or_404(name)
        updatee.x = x
        updatee.y = y

        db.session.commit()
        return "success"
    except:
        return "Something has gone wrong in updating."

@app.route("/manipAttribute/", methods=['POST'])
def manipAttribute():
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
    """Deals with requests from GUI to remove attributes from class."""

    if core_del_attr(name, attr):
        flash("ERROR: Unable to remove attribute " + attr + " from " + name, 'error')

def updateAttribute(name, oldAttr, newAttr):
    """Deals with requests from GUI to update attributes in class."""

    if core_update_attr(name, oldAttr, newAttr):
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
        flash("Invalid arguments, try again", 'error')
    
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
    try:
        rels = Relationship.query.all()

        rel_schema = RelationshipSchema(many=True)
        out = rel_schema.dump(rels)

        return json.dumps(out)
    except:
        return "Error: Unable to get relationship data"