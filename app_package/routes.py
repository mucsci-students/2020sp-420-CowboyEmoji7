"""Connects front-end to back-end.

Contains routes through which requests from
  the view are passed to interact with the data model.
"""

from app_package.models import ClassSchema, SaveSchema
from flask import render_template, json, url_for, request, redirect, flash, Response
from app_package import app, db

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
        new_class = ClassSchema(name=class_name)

        if class_name == '':
            return redirect('/')

        try:
            db.session.add(new_class)
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR: Unable to add Class'

    else:
        # grab all entries in order
        classes = ClassSchema.query.order_by(ClassSchema.date_created).all()
        return render_template('index.html', classes=classes)

@app.route('/delete/<string:name>')
def delete(name):
    """Deals with requests to remove a class.

    Removes the requested class from database, if successful
    """

    class_to_delete = ClassSchema.query.get(name)
    if (class_to_delete == None):
        return 'ERROR: No such class. No changes have been made to your diagram'

    try:
        db.session.delete(class_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'ERROR: Unable to delete Class'

@app.route('/save/', methods=['POST'])
def save():
    """Deals with requests to save current data locally.

    JSONify current data and return the result in a .json file
      as an attachment--to download--with requested name
    """
    try:
        name = request.form['save_name']
        classes = ClassSchema.query.all()

        # Use flask-marshmallow to "jsonify" current data
        class_schema = SaveSchema(many=True)
        out = class_schema.dump(classes)

        # Options utilized strictly for readability of the resulting file
        contents = json.dumps(out, ensure_ascii=False, indent=4)
        return Response(contents, mimetype="application/json", headers={"Content-disposition":"attachment; filename="+ name + ".json;"})
    except:
        return 'ERROR: There was a problem saving. Try again.'

    

@app.route("/load/", methods=['POST'])
def load():
    """Deals with requests to load pre-existing user data from a user's storage.

    Clears current data, then loads file given by user
    Then, adds each datum to the working database and
      redirects to base index to re-render with loaded data
    """

    try:
        Jfile = request.files['file']
        classes = ClassSchema.query.all()
        for item in classes:
            db.session.delete(item)

        data = json.load(Jfile)
        for element in data:
            newClass = ClassSchema(
                name=element["name"],
                x=element["x"],
                y=element["y"]
            )
            db.session.add(newClass)

        db.session.commit()
        return redirect('/')
    except:
        return "ERROR: Unable to load file"
