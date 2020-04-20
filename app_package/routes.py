"""Connects front-end to back-end.

Contains routes through which requests from
  the view are passed to interact with the data model.
"""

from app_package.models import Class, ClassSchema, Relationship, RelationshipSchema, Attribute
from flask import render_template, json, url_for, request, redirect, flash, Response, jsonify
from app_package import app, db, cmd_stack
from app_package.core_func import core_save, core_load, core_parse, core_clear
from app_package.memento.func_objs import (add_class, delete_class, edit_class, 
                                           add_attr, del_attr, edit_attr, add_rel,
                                           del_rel, move)
from parse import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time



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

@app.route('/clear/', methods=['POST'])
def clear():
    """Deals with requests to clear the database."""
    core_clear()
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
                elif action == "DeleteRel":
                    delRelationship(class_name, theDict[el]['to_name'])

    except:
        flash("Invalid arguments, try again.", 'error')
    
    return redirect('/')

def update(oldName, newName):
    """Helper to update a class's name."""
    updateCmd = edit_class(oldName, newName)
    if cmd_stack.execute(updateCmd):
        flash("ERROR: Unable to update class " + oldName + " to " + newName, 'error')

def delAttribute(name, attr):
    """Helper to remove attributes from class."""
    attr_to_del = Attribute.query.get({"class_name":name, "attribute":attr})
    delAttrCmd = del_attr(name, attr, attr_to_del.attr_type)
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


@app.route("/addRelationship/", methods=['POST'])
def addRelationship():
    """Helper function to add relationships to class."""
    try:
        fro = request.form['class_name']
        to = request.form['to']
        rel_type = request.form['rel_type']
        addRelCmd = add_rel(fro, to, rel_type)
        if cmd_stack.execute(addRelCmd):
            flash("ERROR: Unable to add relationship from " + fro + " to " + to, 'error')
    except:
        flash("Invalid arguments, try again.", 'error')

    return redirect('/')


def delRelationship(fro, to):
    """Helper function to remove relationships from class."""
    rel_to_del = Relationship.query.get({"from_name":fro, "to_name":to})
    delRelCmd = del_rel(fro, to, rel_to_del.rel_type)
    if cmd_stack.execute(delRelCmd):
        flash("ERROR: Unable to delete relationship from " + fro + " to " + to, 'error')


@app.route("/getRelationships/", methods=['POST'])
def getRelationship():
    """Helper route to give relationship information to JS."""
    rels = Relationship.query.all()

    rel_schema = RelationshipSchema(many=True)
    out = rel_schema.dump(rels)

    return json.dumps(out)


@app.route("/undo/", methods=['POST'])
def undo():
    """Deals with requests from GUI to undo the last command executed by the user"""
    cmd_stack.undo()
    return redirect('/')


@app.route("/redo/", methods=['POST'])
def redo():
    """Deals with requests from GUI to redo the last command undone by the user"""
    cmd_stack.redo()
    return redirect('/')


@app.route("/export/", methods=['POST'])
def export():
    image_name = request.form['export_name']

    chromeOptions = Options()
    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("--hide-scrollbars")
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chromeOptions)
    driver.get('http://127.0.0.1:5000/')

    height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight )")
    # find name of class furthest right, get element by id, use that as width
    furthestClass = Class.query.order_by(Class.x.desc()).first()
    obj = driver.find_element_by_id(furthestClass.name)
    width = furthestClass.x + obj.rect['width']
    margin = 15
    driver.set_window_size(width + margin, height + margin)

    driver.save_screenshot("%s.png" % image_name)
    driver.close()

    return redirect('/')