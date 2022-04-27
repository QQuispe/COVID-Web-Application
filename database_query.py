import sqlite3
import pandas as pd
from os.path import exists
from os import mkdir

def county_cases_query(county, state, days = 30):
    if(county is None or state is None):
        return None

    con = sqlite3.connect("covid.sqlite")
    #query for the average number of cases in that location over the specified time period
    cases_df = pd.read_sql_query(f"""SELECT avg(replace(replace(cases_per_100k_7_day_count,'suppressed','0'),',','')) as cases 
    FROM cases 
    WHERE date >= DATE('now','{-days} day') AND state_name = '{county}' AND county_name = '{state}'""",
    con)
    if cases_df.empty:
        return None
    else:
        return round(cases_df.cases[0], 1)

#returns the average cases table
#uses pickle to cache results
def get_cases_table(days = 30):
    cache_dir = "cache"
    file_name = cache_dir + f"/pickle{days}.pkl"
    if exists(file_name):
        return pd.read_pickle(file_name)
    else:
        df = avg_cases_table(days)
        if not exists(cache_dir):
            mkdir(cache_dir)
        df.to_pickle(file_name)
        return df


#creates a table of average cases in each county over a number of days
#returns a pandas dataframe
def avg_cases_table(days = 30):
    con = sqlite3.connect("covid.sqlite")
    df = pd.read_sql_query(f"""SELECT state_name, county_name, fips_code, avg(replace(replace(cases_per_100k_7_day_count,'suppressed','0'),',','')) as cases 
    FROM cases 
    WHERE date >= DATE('now','-{days} day')
    GROUP BY fips_code""", con)
    return df

#The same as avg_cases_table, but the value is returned in a format usable for the datatables
def get_avg_cases_json(days = 30):
    return get_cases_table(days).to_dict(orient='records')