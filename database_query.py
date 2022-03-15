from cgi import test
import sqlite3
from numpy import empty
import pandas as pd
import numpy as np

def county_cases_query(county, state):
    con = sqlite3.connect("covid.sqlite")

    #average cases from the past month
    cases_df = pd.read_sql_query(f"""SELECT avg(replace(replace(cases_per_100k_7_day_count,'suppressed','0'),',','')) as cases 
    FROM cases 
    WHERE date >= DATE('now','-31 day') AND state_name = '{county}' AND county_name = '{state}'""",
    con)
    if cases_df.empty:
        return None
    else:
        return round(cases_df.cases[0], 1)