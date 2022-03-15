from flask import Flask, flash, render_template, request, jsonify
from db_test import *
from database_query import *
from database_update import *

app = Flask(__name__)

# Load home page
@app.route('/', methods = ['GET', 'POST'])
def index():
    db = get_db()
    states = db.execute('SELECT DISTINCT state_name from counties').fetchall()
    counties = db.execute('SELECT * FROM counties').fetchall()

    if request.method == 'GET':
        return render_template('home.html',cases = None, map=make_map()._repr_html_(), states = states, counties = counties, state_query = None)
    else:
        state_query = (
            request.form['state_name'],
            request.form['county_name']
        )
        cases = county_cases_query(state_query[0], state_query[1])
        map = make_map()
        return render_template('home.html', cases=cases, map=map._repr_html_(), states = states, counties = counties, state_query = state_query)

# Populate counties per state
@app.route('/county/<state>')
def county(state):
    db = get_db()
    countyArr = []
    counties = db.execute("""SELECT * FROM counties WHERE state_name = ?""", (state,))
    for row in counties:
        countyObj = {
            'state' : row[0],
            'name' : row[1]
        }
        countyArr.append(countyObj)
    return jsonify({'counties': countyArr})

if __name__ == '__main__':
    app.run(debug=True)