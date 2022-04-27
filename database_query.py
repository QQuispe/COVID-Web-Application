from os.path import exists
from os import mkdir
import sqlite3
import pandas as pd

def county_cases_query(county, state, days = 30):
    """
    Returns the average number of cases in a chosen area over a period of time

    Keyword arguments:
    county -- the county or locality
    state -- the state in which that county is located
    days -- the number of preceding days over which to take the average
    """
    if(county is None or state is None):
        return None

    con = sqlite3.connect("covid.sqlite")
    #query for the average number of cases in that location over the specified time period
    cases_df = pd.read_sql_query(f"""
    SELECT avg(replace(replace(cases_per_100k_7_day_count,'suppressed','0'),',','')) as cases 
    FROM cases 
    WHERE date >= DATE('now','-{days} day') AND state_name = '{county}' AND county_name = '{state}'
    """,
    con)
    if cases_df.empty:
        return None
    else:
        return round(cases_df.cases[0], 1)

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
    SELECT state_name, county_name, fips_code, avg(replace(replace(cases_per_100k_7_day_count,'suppressed','0'),',','')) as cases 
    FROM cases 
    WHERE date >= DATE('now','-{days} day')
    GROUP BY fips_code
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
