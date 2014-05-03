from flask import Flask, render_template, flash, redirect
from flask import request, redirect, make_response
from forms import LoginForm
import helpers
import csv 
import os


app = Flask(__name__)
app.secret_key= "asdfaewra"

@app.route('/')
@app.route('/index', methods = ['GET', 'POST'])
def index():
    f = open("csvs/results.csv", "w")
    f.truncate()
    f.close()
    form = LoginForm()
    return render_template('index.html', 
        title = 'Enter Info',
        form = form)


@app.route('/data', methods=['POST'])
def handle_data():
    form = LoginForm()
    names = request.form['users']
    print names
    scrape(names)
    return render_template('index.html', 
        title = 'Enter Info',
        form = form)

@app.route('/results', methods=['GET', 'POST'])
def display_results():
    names = request.form['users']
    scrape(names)
    return render_template('results.html')


@app.route('/download')
def download():
    data = ""
    with open('csvs/results.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in reader:
            data = data + ', '.join(row) + '\n'
    # We need to modify the response, so the first thing we 
    # need to do is create a response out of the CSV string
    response = make_response(data)
    # This is the key: Set the right header for the response
    # to be downloaded, instead of just printed on the browser
    response.headers["Content-Disposition"] = "attachment; filename=results.csv"
    return response


def scrape(ig_handles):
    username = ig_handles
    filename = "results"
    people = username.split(",")

    open('csvs/' + filename + '.csv', 'w').close()

    for person in people:
        helpers.main(person, filename)

if __name__ == '__main__':
        app.run(debug=True)