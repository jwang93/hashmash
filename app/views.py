from flask import Flask, render_template, flash, redirect
from flask import request, redirect
from forms import LoginForm
import helpers


app = Flask(__name__, static_url_path='')
app.secret_key= "asdfaewra"

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
    scrape(names)
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

if __name__ == '__main__':
        app.run(debug=True)