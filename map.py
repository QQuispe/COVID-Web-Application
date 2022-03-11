from flask import Flask, flash, render_template, request
from db_test import *
from test_query import *

app = Flask(__name__)

# Load home page
@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        state_query = (
            request.form['state_name'],
            request.form['county_name']
        )
        cases = round(query_db(state_query), 2)
        map = exploration_and_cleaning()
        return render_template('home.html', cases=cases, map=map._repr_html_())

if __name__ == '__main__':
    app.run(debug=True)