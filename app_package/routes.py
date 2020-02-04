from app_package.models import ClassSchema
from flask import render_template, url_for, request, redirect, flash
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


@app.route('/update/<string:name>', methods=['GET', 'POST'])
def update(name):
    task = ClassSchema.query.get_or_404(name)

    if request.method == 'POST':
        # set task content to form input
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR: There was an issue updating your Class'
    else:
        return render_template('update.html', task=task)