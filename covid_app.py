"""
Flask app for managing the website
"""
from flask import Flask, render_template, request, jsonify
from map import make_map
from database_query import get_avg_cases_json, county_cases_query
from database_update import get_db

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    """
    Home page of the website
    """
    database = get_db()
    states = database.execute('SELECT DISTINCT state_name from counties').fetchall()
    counties = database.execute('SELECT * FROM counties').fetchall()

    if request.method == 'GET':
        return render_template('home.html',
        cases = None,
        map=make_map(),
        states = states, counties = counties,
        state_query = None)
    state_query = (
        request.form['state_name'],
        request.form['county_name']
    )
    cases = county_cases_query(state_query[0], state_query[1])
    return render_template('home.html', cases=cases, map=make_map(), states = states, counties = counties, state_query = state_query)

# Testing page
@app.route('/test', methods = ['GET', 'POST'])
def maptest():
    """
    Test Page
    """
    database = get_db()
    states = database.execute('SELECT DISTINCT state_name from counties').fetchall()
    counties = database.execute('SELECT * FROM counties').fetchall()

    if request.method == 'GET':
        return render_template(
            'test_home.html',
            cases = None,
            map = make_map(),
            states = states,
            counties = counties,
            state_query = None,
            cases_table = get_avg_cases_json()
            )

@app.route('/compare', methods = ['GET', 'POST'])
def map2test():
    """
    Comparison Test Page
    """
    database = get_db()
    states = database.execute('SELECT DISTINCT state_name from counties').fetchall()
    counties = database.execute('SELECT * FROM counties').fetchall()

    if request.method == 'GET':
        return render_template(
            'compare.html',
            cases = None, 
            map=make_map(),
            states = states,
            counties = counties,
            state_query = None,
            cases_table = get_avg_cases_json()
            )


# Populate counties per state
@app.route('/county/<state>')
def county(state):
    """
    Find a list of counties in a given state
    """
    database = get_db()
    county_arr = []
    counties = database.execute("""SELECT * FROM counties WHERE state_name = ?""", (state,))
    for row in counties:
        county_obj = {
            'state' : row[0],
            'name' : row[1]
        }
        county_arr.append(county_obj)
    return jsonify({'counties': county_arr})

if __name__ == '__main__':
    app.run(debug=True)
