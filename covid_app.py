"""
Flask app for managing the website
"""
from flask import Flask, render_template, request, jsonify
from map import make_map
from database_query import get_avg_cases_json, county_cases_query, get_county_results
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
    cases_table = get_avg_cases_json()

    if request.method == 'GET':
        return render_template('home.html',
        total_cases = 0, total_deaths = 0, vaccination_stat = 0, cases_per_stat = 0,
        map=make_map(),
        states = states, counties = counties,
        cases_table = cases_table
        )
    state_query = (
        request.form['state_name'],
        request.form['county_name']
    )
    days = request.form['days']
    total_cases, total_deaths, vaccination_stat, cases_per_stat = get_county_results(cases_table, state_query)
    results_message = "Results for " +  state_query[1] + ", " + state_query[0] + " over the last " + days + " day(s):"


    return render_template('home.html',
        map=make_map(),
        states = states,
        counties = counties,
        days = days,
        results_message = results_message,
        cases_table = cases_table,
        total_cases = total_cases,
        total_deaths = total_deaths,
        vaccination_stat = vaccination_stat,
        cases_per_stat = cases_per_stat,
        )

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