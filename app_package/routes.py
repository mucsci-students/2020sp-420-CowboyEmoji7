"""Connects front-end to back-end.

Contains routes through which requests from
  the view are passed to interact with the data model.
"""

from app_package.models import ClassSchema, SaveSchema
from flask import render_template, json, url_for, request, redirect, flash, Response
from app_package import app, db
from app_package.core_func import core_add, core_delete, core_save, core_load


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
            return 'ERROR: Unable to add Class'
        return redirect('/')

    else:
        # grab all entries in order
        classes = ClassSchema.query.order_by(ClassSchema.date_created).all()
        return render_template('index.html', classes=classes)


@app.route('/delete/<string:name>')
def delete(name):
    """Deals with requests to remove a class.

    Removes the requested class from database, if successful
    """

    if core_delete(name):
        return 'ERROR: Unable to delete Class'
    return redirect('/')


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

    Jfile = request.files['file']
    try:
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

        updatee = ClassSchema.query.get_or_404(name)
        updatee.x = x
        updatee.y = y

        db.session.commit()
        return "success"
    except:
        return "Something has gone wrong in updating."
