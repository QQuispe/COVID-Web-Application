import sqlite3
import pandas as pd
from sodapy import Socrata
from flask import g

data_addr = "https://data.cdc.gov/resource/nra9-vzzn.json"


data_url='data.cdc.gov'    # The Host Name for the API endpoint
cases_data_set='nra9-vzzn' # Covid Cases data set
vaccinations_data_set='8xkx-amqh' # Covid vaccinations dataset

def update_db():
    # Socrata API key
    app_token ='5FoiIo91nIpvXhetFuJ9yNAPA'

    client = Socrata(data_url, app_token)      # Create the client to point to the API endpoint
    # Set the timeout to 4 minutes
    client.timeout = 240

    # Setting an excessively high limit to make sure all records are retrieved
    # TODO change these queries to only retrieve new records
    cases_df = pd.DataFrame.from_records(client.get(cases_data_set, limit = 100000000))
    vaccinations_df = pd.DataFrame.from_records(client.get(vaccinations_data_set, limit = 100000000))

    #open connection to the database
    con = sqlite3.connect("covid.sqlite")
    cases_df.to_sql("cases", con, if_exists="replace")
    vaccinations_df.to_sql("vaccinations",con, if_exists="replace")
    con.close()

    create_states_table()

def create_states_table():
    con = sqlite3.connect("covid.sqlite")
    cur = con.cursor()
    cur.execute('CREATE TABLE counties AS SELECT DISTINCT state_name, county_name from cases ORDER BY state_name, county_name ASC')
    con.commit()
    con.close()

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('covid.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

if __name__ == '__main__':
    update_db()