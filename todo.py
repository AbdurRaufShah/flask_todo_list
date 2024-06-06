from flask import Flask, render_template,request,sessions, redirect,url_for,flash
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'key'
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column (db.String(200), nullable= False)

with app.app_context():
    db.create_all()


@app.route('/', methods= ['GET','POST'])
@app.route('/<int:todo_id>', methods = ['GET','POST'])
def todo(todo_id=None):
    if request.method == 'POST':
        title = request.form.get('title')
        if todo_id is None :
            todo = Todo(title=title)
            db.session.add(todo)
            db.session.commit()
            flash("Todo item added successfully",'Success')
        else:
            todo = Todo.query.get(todo_id)
            if todo:
                todo.title = title
                db.session.commit()
                flash("Todo item updated successfully",'Success')

        return redirect(url_for('todo'))
    
    todo = None
    if todo_id is not None:
        todo = Todo.query.get(todo_id)    
    todos = Todo.query.order_by(Todo.id.desc()).all()    
    return render_template("todo.html", todos = todos, todo = todo)
        


 
@app.route('/todo-delete/<int:todo_id>',methods = ['POST'])
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash("Todo item Deleted successfully",'Success')
    
    return redirect(url_for('todo'))


if __name__ == '__main__':
    app.run(debug=True, port=3000)
