from flask import Flask, render_template, url_for, request, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'b5de70f8ba9137f8bc7e5d1df81f1e70' 
#'super puper secret key'

app.config['SQLALCHEMY_DATABASE_URI'] =    	'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 	False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, 	primary_key = True)
    name = db.Column(db.String(200), nullable=False) 
    email = db.Column(db.String(120), nullable=False, unique = True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow)
   
    def __repr__(self):
        return f"<Name>: {self.name}"

class FirstForm(FlaskForm):
    name = StringField("Enter your name, please", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserForm(FlaskForm):
    name=StringField("Name", validators=[DataRequired()])
    email=StringField("Email", validators=[DataRequired()])
    submit = SubmitField('Submit')

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

game = { }

def init():
    game['choise']=None
    game['comp_win'] = 0
    game['you_win'] =0
    game['round'] = 0

@app.route('/start/')
def start():
    init()
    return render_template('rsp.jinja', start=True)

@app.route('/game/')
def rsp():
    
    if game['round'] < 5:
        game['round'] +=1
        print(game)
        n = random.randint(0,2)
        if game['choise'] == '0' and n == 0:
            flash('Draw')
        elif game['choise'] == '0' and n == 1:
            flash('You win')
            game['you_win'] +=1
        elif game['choise'] == '0' and n == 2:
            flash('Comp win')
            game['comp_win'] += 1
        else:
            pass
    
    else:
        if game['comp_win'] > game['you_win']:
            flash('Total com win')
        elif game['comp_win'] == game['you_win']:
            flash('Total draw')
        else:
            flash('Total you win')
    return render_template('rsp.jinja')

@app.route('/select/<ch>')
def select(ch):
    game['choise'] = ch
    return redirect(url_for('rsp'))

@app.route('/user/add/', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    our_users = []
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
            flash(f'User {form.name.data} added successfully', category='success')
        else:
            flash(f'User {form.name.data} cannot be added', category='danger')
        
        form.name.data = ''
        form.email.data = ''
        our_users = Users.query.order_by(Users.date_added)

    return render_template('lecture5.jinja', form=form, our_users=our_users)


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
    name = None
    form = FirstForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('lecture3.jinja', name = name, form = form )  





