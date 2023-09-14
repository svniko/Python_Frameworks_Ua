from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template('hello.html.jinja', name='Mary')

@app.route("/user/<name>")
def user(name):
    return f"<h1>Hello, {name}<h1>"


@app.route("/<name>")
def hello_user(name):
    age = 21
    return render_template('hello.html.jinja', 
                           name=name, 
                           age=age)

@app.route("/hello")
def greeting():
    name, age, prof = 'Jerry', 24, 'Programmer'
    temp_context = dict(name=name, age=age, prof=prof)
    return render_template('hello.html.jinja', 
                           **temp_context)

@app.route("/about")
def about():
    return render_template('about.jinja')