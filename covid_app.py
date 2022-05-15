"""
Flask app for managing the website
"""
from flask import Flask, render_template, request, jsonify
from map import make_map
from database_query import get_avg_cases_json, get_counties_in_state, get_county_results, get_states, get_counties, get_counties_in_state

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    """
    Home page of the website
    """
    
    states = get_states()
    counties = get_counties()
    cases_table = get_avg_cases_json()

    if request.method == 'GET':
        state_query = ("Maryland", "Montgomery County")
        days = 30
    else:
        state_query = (request.form['state_name'], request.form['county_name'])
        days = request.form['days']
    cases_table = get_avg_cases_json(days)
    total_cases, total_deaths, risk_level, cases_per_stat = get_county_results(cases_table, state_query)
    results_message = f"Results for {state_query[1]}, {state_query[0]} over the last {days} days:"


    return render_template('home.html',
        map=make_map(days),
        states = states,
        counties = counties,
        days = days,
        results_message = results_message,
        cases_table = cases_table,
        total_cases = total_cases,
        total_deaths = total_deaths,
        risk_level = risk_level,
        cases_per_stat = cases_per_stat,
        )
@app.route('/compare', methods = ['GET', 'POST'])
def map2test():
    """
    Comparison Test Page
    """
    states = get_states()
    counties = get_counties()

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
    
    county_arr = []
    counties = get_counties_in_state(state)
    for row in counties:
        county_obj = {
            'state' : row[0],
            'name' : row[1]
        }
        county_arr.append(county_obj)
    return jsonify({'counties': county_arr})

if __name__ == '__main__':
    app.run(debug=True)