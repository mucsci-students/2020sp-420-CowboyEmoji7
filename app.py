from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#testing Commit 

app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newtest.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    name = db.Column(db.String(200), primary_key=True)
    content = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route ('/', methods=['POST', 'GET'])
def index ():
    if request.method == 'POST':
        #form tag 'content'
        class_name = request.form['class_name']
        new_task = Todo(name=class_name)

        if class_name == '':
            return redirect ('/')

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR: Unable to add Class'

    else:
        #grab all entries in order
        classes = Todo.query.order_by(Todo.date_created).all()
        return render_template ('index.html', classes=classes)

@app.route('/delete/<string:name>')
def delete(name):
    class_to_delete = Todo.query.get_or_404(name)

    try:
        db.session.delete(class_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'ERROR: Unable to delete Class'

@app.route('/update/<string:name>',methods=['GET','POST'])
def update(name):
    task = Todo.query.get_or_404(name)

    if request.method == 'POST':
        #set task content to form input
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'ERROR: There was an issue updating your Class'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run (debug=True)