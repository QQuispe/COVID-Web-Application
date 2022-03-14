from flask import Flask, flash, render_template, request
from db_test import *
from test_query import *
from database_update import *

app = Flask(__name__)

# Load home page
@app.route('/', methods = ['GET', 'POST'])
def index():
    db = get_db()
    states = db.execute('SELECT DISTINCT state_name from counties').fetchall()
    counties = db.execute('SELECT * FROM counties').fetchall()

    if request.method == 'GET':
        return render_template('home.html',cases = None, map=make_map()._repr_html_(), states = states, counties = counties)
    else:
        state_query = (
            request.form['state_name'],
            request.form['county_name']
        )
        cases = query_db(state_query)
        map = make_map()
        return render_template('home.html', cases=cases, map=map._repr_html_(), states = states, counties = counties)

if __name__ == '__main__':
    app.run(debug=True)