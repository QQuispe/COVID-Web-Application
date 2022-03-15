from cgi import test
import sqlite3
from numpy import empty
import pandas as pd
import numpy as np

def county_cases_query(county, state):
    con = sqlite3.connect("covid.sqlite")

    #get all cases from the past month
    cases_df = pd.read_sql_query(f"""SELECT cases_per_100k_7_day_count as cases 
    FROM cases 
    WHERE date >= DATE('now','-31 day') AND state_name = '{county}' AND county_name = '{state}' ORDER BY date DESC""",
    con)
    if cases_df.empty:
        return None
    
    #convert cases to a numeric data type
    #change suppressed to zero
    cases_df.loc[cases_df.cases == "suppressed",'cases'] = "0"
    #remove commas
    cases_df.cases = cases_df.cases.apply(lambda x: x.replace(',',''))
    #now cases can be converted to a numeric data type
    cases_df.cases = cases_df.cases.astype(float)

    val = np.mean(cases_df.cases)
    return round(val, 1)