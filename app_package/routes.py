from app_package.models import ClassSchema, SaveSchema
from flask import render_template, json, url_for, request, redirect, flash, Response
from app_package import app, db


@app.route('/', methods=['POST', 'GET'])
def index():
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
    class_to_delete = ClassSchema.query.get_or_404(name)

    try:
        db.session.delete(class_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'ERROR: Unable to delete Class'


@app.route('/save/', methods=['POST'])
def save():
    name = request.form['save_name']

    classes = ClassSchema.query.all()
    class_schema = SaveSchema(many=True)
    out = class_schema.dump(classes)

    contents = json.dumps(out, ensure_ascii=False, indent=4)
    return Response(contents, mimetype="application/json", headers={"Content-disposition":"attachment; filename="+ name + ".json;"})


@app.route("/load/", methods=['POST'])
def load():

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
