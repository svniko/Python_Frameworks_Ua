from flask import Flask, render_template, url_for, request

app = Flask(__name__)

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





