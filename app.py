
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

# Creating the database tables
with app.app_context():
    db.create_all()

@app.route('/',methods=['GET','POST']) #'/' is binded to the home function defined further
def home(): 
    if request.method=='POST':
       title = request.form['title']
       desc = request.form['desc']
       todo =Todo(title=title, desc=desc)
       db.session.add(todo)
       db.session.commit()

    allTodo=Todo.query.all()
    return render_template("home.html",alltodo=allTodo)

@app.route('/delete/<int:sno>') #The sno which is to be deleted is passed to the function
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first() #filtering the table based on the sno
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>', methods=['GET','POST']) #the sno for which the update button is pressed is passed to the update function
def update(sno):
    if request.method=='POST':
       title = request.form['title']
       desc = request.form['desc']
       todo=Todo.query.filter_by(sno=sno).first()
       todo.title=title
       todo.desc=desc
       db.session.add(todo)
       db.session.commit()
       return redirect('/')
    
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)
 


if __name__ == "__main__":
    app.run(debug=True)
