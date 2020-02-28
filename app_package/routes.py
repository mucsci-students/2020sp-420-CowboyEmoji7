"""Connects front-end to back-end.

Contains routes through which requests from
  the view are passed to interact with the data model.
"""

from app_package.models import Class, Attribute
from flask import render_template, json, url_for, request, redirect, flash, Response
from app_package import app, db
from app_package.core_func import (core_add, core_delete, core_save, core_update,
                                   core_load, core_add_attr, core_del_attr, 
                                   core_update_attr, core_add_rel, core_del_rel)


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

        if core_add(class_name):
            flash('ERROR: Unable to add Class', 'error')
        return redirect('/')

    else:
        # grab all entries in order
        classes = Class.query.order_by(Class.date_created).all()
        attributes = Attribute.query.order_by(Attribute.date_created).all()
        return render_template('index.html', classes=classes, attributes=attributes)


@app.route('/addattr/<string:name>', methods=['POST', 'GET'])
def add_attr(name):
    """Deals with requests to add an attribute to a class.

    Adds the requested attribute to the database, if successful
    """
    
    attrName = request.form[name+'-attribute']
    flash(attrName, 'error')
    attrList = attrName.split()
    for attr in attrList:
        flash(attr, 'error')
        if core_add_attr(name, attr):
            flash('ERROR: Unable to add Attribute '+attr, 'error')
    return redirect('/')



@app.route('/delete/<string:name>')
def delete(name):
    """Deals with requests to remove a class.

    Removes the requested class from database, if successful
    """

    if core_delete(name):
        flash('ERROR: Unable to delete Class', 'error')
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
            return "ERROR: Unable to update class"
        return redirect('/')
    except:
        return "Invalid arguments, try again."


@app.route('/save/', methods=['POST'])
def save():
    """Deals with requests to save current data locally.

    JSONify current data and return the result in a .json file
      as an attachment--to download--with requested name
    """
    try:
        name = request.form['save_name']
    except:
        return "There was a problem saving. Try again."

    contents = core_save()
    if contents is None:
        return "There was a problem saving. Try again."
    return Response(contents, mimetype="application/json", headers={"Content-disposition": "attachment; filename=" + name + ".json;"})
 


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
            return "ERROR: Unable to load data into database"
        return redirect('/')
    except:
        return "Invalid JSON"


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

@app.route("/addAttribute/", methods=['POST'])
def addAttribute():
    """Deals with requests from GUI to add attributes to class."""
    try:
        class_name = request.form['class_name']
        attribute = request.form['attribute']

        if core_add_attr(class_name, attribute):
            return "ERROR: Unable to add attribute"
        return redirect('/')
    except:
        return "Invalid arguments, try again"

@app.route("/delAttribute/", methods=['POST'])
def delAttribute():
    """Deals with requests from GUI to remove attributes from class."""
    try:
        class_name = request.form['class_name']
        attribute = request.form['attribute']

        if core_del_attr(class_name, attribute):
            return "ERROR: Unable to remove attribute"
        return redirect('/')
    except:
        return "Invalid arguments, try again"

@app.route("/updateAttribute", methods=['POST'])
def updateAttribute():
    """Deals with requests from GUI to update attributes in class."""
    try:
        class_name = request.form['class_name']
        attribute = request.form['attribute']
        new_attr = request.form['new_attribute']

        if core_update_attr(class_name, attribute, new_attr):
            return "ERROR: Unable to edit attribute"
        return redirect('/')
    except:
        return "Invalid arguments, try again"

@app.route("/addRelationship/", methods=['POST'])
def addRelationship():
    """Deals with requests from GUI to add relationships to class."""
    try:
        fro = request.form['class_name']
        to = request.form['relationship']

        if core_add_rel(fro, to):
            return "ERROR: Unable to add relationship"
        return redirect('/')
    except:
        return "Invalid arguments, try again"

@app.route("/delRelationship/", methods=['POST'])
def delRelationship():
    """Deals with requests from GUI to remove relationships from class."""
    try:
        fro = request.form['class_name']
        to = request.form['relationship']

        if core_del_rel(fro, to):
            return "ERROR: Unable to remove relationship"
        return redirect('/')
    except:
        return "Invalid arguments, try again"