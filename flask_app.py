from flask import Flask, render_template, url_for, request, redirect, session, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b5de70f8ba9137f8bc7e5d1df81f1e70' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#'super puper secret key'

class FirstForm(FlaskForm):
    name = StringField("Enter your name, please", validators=[DataRequired()])
    submit = SubmitField("Submit")



class Users(db.Model):
    id = db.Column(db.Integer, 	primary_key = True)
    name = db.Column(db.String(200), nullable=False) 
    email = db.Column(db.String(120), nullable=False, unique = True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'<Name>: {self.name}'  


pets = [
    {
        'kind':'cat',
        'name':'Tom',
        'age':10,
        'color':'grey'
    },
    {
        'kind':'cat',
        'name':'Barsic',
        'age':5,
        'color':'white'
    },
    {
        'kind':'dog',
        'name':'Spike',
        'age':7,
        'color':'brown'
    },
]


@app.route("/")
def hello_world():
    return render_template('hello.html.jinja', name='Mary')

@app.route("/user/<name>/")
def user(name):
    return f"<h1>Hello, {name}<h1>"


@app.route("/users/<name>/")
def hello_user(name):
    age = 21
    return render_template('hello.html.jinja', 
                           name=name, 
                           age=age)

@app.route("/hello/")
def greeting():
    name, age, prof = 'Jerry', 24, 'Programmer'
    temp_context = dict(name=name, age=age, prof=prof)
    return render_template('hello.html.jinja', 
                           **temp_context)

@app.route("/about/")
def about():
    return render_template('about.jinja')

@app.route('/pets/')
def pet():
    return render_template('pets.jinja', pets = pets, title="Out pets")

@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.jinja"), 404

@app.route('/hi/', methods=['GET','POST'])
def smb():
    if request.method == 'GET':
        return render_template('hi.jinja', name='Stranger')
    else:
        name = request.form.get('name')
        if not name:
            return render_template('lecture2.jinja', flag=0)
        return render_template('hi.jinja', name=name)

@app.route('/lect2/')
def lect2():
    return render_template('lecture2.jinja')

@app.route('/lect3/', methods=['GET', 'POST'])
def lect3():
    # name = None
    form = FirstForm()
    if form.validate_on_submit():
        n = form.name.data
        if len(n) < 3:
            flash('Looks like your name is too short')
            return redirect(url_for('lect3'))
        session['name'] = n
        name = form.name.data
        form.name.data = ''
        return redirect(url_for('lect3'))
    return render_template('lecture3.jinja', 
                            name = session.get('name'), 
                            # name=name,
                            form = form )  





