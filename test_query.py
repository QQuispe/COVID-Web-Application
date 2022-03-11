from cgi import test
import sqlite3
import folium
import pandas as pd

def query_db(query):
    (x, y) = query
    con = sqlite3.connect("covid.sqlite")
    cur = con.cursor()
    cases_df = pd.read_sql_query("SELECT * FROM cases WHERE date >= DATE('now','-31 day') ORDER BY date DESC", con)
    cases_df = cases_df.rename(columns={'cases_per_100k_7_day_count' : 'cases','percent_test_results_reported':'test_percent','community_transmission_level' : 'severity'  })
    #change suppressed to zero
    cases_df.loc[cases_df.cases == "suppressed",'cases'] = "0"
    #remove commas
    cases_df.cases = cases_df.cases.apply(lambda x: x.replace(',',''))
    #now cases can be converted to a numeric data type
    cases_df.cases = cases_df.cases.astype(float)
    #change None to zero
    cases_df.test_percent.fillna("0", inplace = True)
    #remove commas
    cases_df.test_percent = cases_df.test_percent.apply(lambda x: x.replace(',',''))
    #now test percent can be converted to a numeric data type
    cases_df.test_percent = cases_df.test_percent.astype(float)
    cases_df.state_name = cases_df.state_name.astype('string') 
    cases_df.county_name = cases_df.county_name.astype('string') 

    test_df = cases_df.groupby(['state_name','county_name'])[['cases']].mean()
    test_df = test_df.reset_index()
    return test_df[(test_df.state_name == x) & (test_df.county_name == y)]['cases'].item() 