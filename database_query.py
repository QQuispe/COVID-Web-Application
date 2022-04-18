import sqlite3
import pandas as pd
from database_update import get_db

def county_cases_query(county, state, days = 31):
    con = sqlite3.connect("covid.sqlite")

    #average cases from the past month
    cases_df = pd.read_sql_query(f"""SELECT avg(replace(replace(cases_per_100k_7_day_count,'suppressed','0'),',','')) as cases 
    FROM cases 
    WHERE date >= DATE('now','{-days} day') AND state_name = '{county}' AND county_name = '{state}'""",
    con)
    if cases_df.empty:
        return None
    else:
        return round(cases_df.cases[0], 1)

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
def avg_cases_json(days = 30):
    df = get_db().execute(
        f"""SELECT state_name, county_name, fips_code, avg(replace(replace(cases_per_100k_7_day_count,'suppressed','0'),',','')) as cases 
        FROM cases 
        WHERE date >= DATE('now','-{days} day')
        GROUP BY fips_code"""
        ).fetchall()
    return df