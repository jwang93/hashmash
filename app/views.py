from flask import render_template, flash, redirect
from flask import request, redirect
from app import app
from forms import LoginForm
import helpers


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


def scrape(ig_handles):
    username = ig_handles
    filename = "results"
    people = username.split(",")

    open('csvs/' + filename + '.csv', 'w').close()

    for person in people:
        helpers.main(person, filename)