from flask import Flask, render_template, flash, redirect
from flask import request, redirect, make_response
from forms import LoginForm
import helpers
import csv 
import os


app = Flask(__name__)
app.secret_key= "asdfaewra"
invalid_accounts = []


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

@app.route('/results', methods=['GET', 'POST'])
def display_results():
    names = request.form['users']
    scrape(names)
    if scrape(names) ==  1:
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
    else:
        return render_template('error.html')


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


# Return 1 if all accounts are valid, 0 otherwise 
def scrape(ig_handles):
    username = ig_handles
    filename = "results"
    people = username.split(",")
    invalid_accounts = []

    open('csvs/' + filename + '.csv', 'w').close()

    for person in people:
        if helpers.main(person.strip(), filename) == -1:
            invalid_accounts.append(str(person))
            print str(person) + " is an invalid or private Instagram account." 

    if len(invalid_accounts) > 0:
        return 0
    else:
        return 1

if __name__ == '__main__':
        app.run(debug=True)