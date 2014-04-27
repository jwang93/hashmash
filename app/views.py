from flask import render_template, flash, redirect
from flask import request, redirect
from app import app
from forms import LoginForm

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = LoginForm()
    return render_template('index.html', 
        title = 'Enter Info',
        form = form)


@app.route('/data', methods=['POST'])
def handle_data():
    form = LoginForm()
    names = request.form['users']
    print names
    return render_template('index.html', 
        title = 'Enter Info',
        form = form)