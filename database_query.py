"""
This module provides functions for interacting with the database
and performing certain queries
"""
from os.path import exists
from os import mkdir
import sqlite3
import pandas as pd
from database_update import get_db

def get_cases_table(days = 30):
    """
    Returns a dataframe with the average covid statistics over a period of time.
    Pulls cached results if available, otherwise queries the database.

    Keyword arguments:
    days -- the number of preceding days over which to aggregate the data (default 30)
    """
    cache_dir = "cache"
    file_name = cache_dir + f"/pickle{days}.pkl"
    if exists(file_name):
        return pd.read_pickle(file_name)
    cases_df = avg_cases_table(days)
    if not exists(cache_dir):
        mkdir(cache_dir)
    cases_df.to_pickle(file_name)
    return cases_df


def avg_cases_table(days = 30):
    """
    Create a dataframe with county level data aggregated over a period of time

    Keyword arguments:
    days -- the number of days over which to aggregate data
    """
    con = sqlite3.connect("covid.sqlite")
    table = pd.read_sql_query(f"""
    SELECT
        a.fips_code as fips_code, risk_level, state_name,
         county_name, total_cases, total_deaths, cases_per_cap
    FROM
        (
        SELECT DISTINCT
            fips_code, state_name, county_name,
            last_value(community_transmission_level) OVER (
                PARTITION BY fips_code
                ORDER BY date ASC
                RANGE BETWEEN UNBOUNDED PRECEDING AND 
                UNBOUNDED FOLLOWING
            ) as risk_level
        FROM merged
        ) AS a
        JOIN
        (
        SELECT fips_code, CAST(max(cases) - min(cases) AS INT) as total_cases,
            CAST(max(deaths) - min(deaths) AS INT) as total_deaths, avg(cases_daily) as cases_per_cap
        FROM merged 
        WHERE date >= DATE('now','-{days} day')
        GROUP BY fips_code
        HAVING total_deaths IS NOT NULL
        ) AS b
        ON a.fips_code = b.fips_code
    """,
    con)
    return table

#The same as avg_cases_table, but the value is returned in a format usable for the datatables
def get_avg_cases_json(days = 30):
    """"
    Create an table of aggregated county level data in json format

    Keyword arguments:
    days -- the period of time over which to aggregate the data (default 30)
    """
    return get_cases_table(days).to_dict(orient='records')

def get_county_results(table, state_query):
    """
    Get relevant COVID iformation from cases_table based on selected county

    Keyword arguments:
    table -- cases table from above
    state_query -- name of county and state that was selected on main form
    """
    county_name = state_query[1]
    state_name = state_query[0]

    county_row = (next(item for item in table if item['state_name'] == state_name and item['county_name'] == county_name))

    # Map matched county's data to values that will be returned to front end
    for k, v in county_row.items():
        if k == 'total_cases':
            total_cases = v
        if k == 'total_deaths':
            total_deaths = v
        if k == 'risk_level':
            risk_level = v
        if k == 'cases_per_cap':
            cases_per_stat = round(v, 1)
    return total_cases, total_deaths, risk_level, cases_per_stat

def get_states():
    """
    Get a list of states
    """
    return get_db().execute('SELECT DISTINCT state_name from counties').fetchall()

def get_counties():
    """
    Get a table of states and counties
    """
    return get_db().execute('SELECT * FROM counties').fetchall()

def get_counties_in_state(state):
    """
    Find all counties in a certain state
    """
    return get_db().execute("""SELECT * FROM counties WHERE state_name = ?""", (state,))