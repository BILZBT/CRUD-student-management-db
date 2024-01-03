from flask import Flask, request, redirect,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Student.sqlite3'
app.config['SECRET_KEY']='0011'
db=SQLAlchemy(app)
class students(db.Model):
     id=db.Column('ID',db.Integer,primary_key=True)
     name=db.Column(db.String(50))
     age=db.Column(db.Integer)
     def __init__(self,name,age):
         self.name=name
         self.age=age
         
@app.route('/')
def web():
    details=students.query.all()
    return render_template('index.html',details=details)    
@app.route('/add',methods=['POST','GET'])
def add_details():
    if request.method=='POST':
        name=request.form['name']
        age=request.form['age']
        student=students(name,age)
        db.session.add(student)
        db.session.commit()  
        return redirect(url_for('web'))
    return render_template('add.html')
@app.route('/delete/<int:id>')
def delete_data(id):
    person=students.query.get(id)
    db.session.delete(person)
    db.session.commit()
    return redirect(url_for('web'))
@app.route('/edit/<int:id>',methods=['POST','GET'])
def edit_data(id):
    person=students.query.get(id)
    if request.method=='POST':
        person.name=request.form['name']
        person.age=request.form['age']
        db.session.commit()
        return redirect(url_for('web'))
    return render_template('edit.html',person=person)
        
        
    


if __name__==('__main__'):
    with app.app_context():
        db.create_all()
    app.run(debug=True)    
