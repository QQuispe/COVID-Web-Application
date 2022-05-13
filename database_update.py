"""
This module is used to update the database as well as manage various other data sources
"""

import sqlite3
import json
from os.path import exists, join
from os import listdir, remove
from urllib.request import urlopen
import pandas as pd
from sodapy import Socrata
from flask import g


import geopandas as gpd

#local file for geojson shapes of counties
COUNTIES_FILE = 'counties_geo.json'

CDC_DATA_REPO='data.cdc.gov'    # The Host Name for the API endpoint
CDC_CASES_ID='nra9-vzzn' # Covid Cases data set
CDC_VAX_ID='8xkx-amqh' # Covid vaccinations dataset
SOCRATA_TOKEN ='5FoiIo91nIpvXhetFuJ9yNAPA' # Socrata API key
COUNTY_GEOJSON_URL = "https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json"
NYTIMES_COUNTIES_URL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
NYTIMES_2022_LINK = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2022.csv"

DB_FILE = "covid.sqlite"

def update_db():
    """
    Downloads the daily case data table and inserts it into the database
    """

    update_cdc()
    update_nytimes()
    create_states_table()
    merge_tables()
    clear_cache()

def update_cdc():
    """
    Downloads the daily cdc case data table and inserts it into the database
    """

    # Create the client to point to the API endpoint
    client = Socrata(CDC_DATA_REPO, SOCRATA_TOKEN)
    # Set the timeout to 4 minutes
    client.timeout = 240

    # Setting an excessively high limit to make sure all records are retrieved
    cases = client.get(CDC_CASES_ID, limit = 100000000)
    cases_df = pd.DataFrame.from_records(cases)

    #open connection to the database
    con = sqlite3.connect(DB_FILE)
    cases_df.to_sql("cdc", con, if_exists="replace")
    #vaccinations_df.to_sql("vaccinations",con, if_exists="replace")
    con.close()

def update_nytimes():
    """
    Downloads data from the New York Times
    """
    ny_df = pd.read_csv(NYTIMES_COUNTIES_URL, index_col=0)
    con = sqlite3.connect(DB_FILE)
    ny_df.to_sql("nytimes", con, if_exists="replace")
    con.close()

def merge_tables():
    """"
    Merge the nytimes and cdc tables
    """
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    cur.execute("""
    SELECT count(name)
    FROM sqlite_master
    WHERE type='table' AND name='merged'
    """)
    if cur.fetchone()[0] > 0:
        cur.execute("DROP TABLE merged")
    cur.execute("""
    CREATE TABLE merged AS 
    SELECT *, replace(replace(cases_per_100k_7_day_count,'suppressed','0'),',','') as cases_weekly
    FROM cdc c
    JOIN nytimes n
    ON c.fips_code = n.fips AND DATE(c.date) = n.date
    ORDER BY state_name, county_name, date ASC""")
    con.commit()
    con.close()

def create_states_table():
    """
    Create table containing just the states and their counties.
    This is an often used query.
    """
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()
    #check if table already exists
    cur.execute("""
    SELECT count(name)
    FROM sqlite_master
    WHERE type='table' AND name='counties'
    """)
    if(cur.fetchone()[0] == 0):
        cur.execute("""
        CREATE TABLE counties AS 
        SELECT DISTINCT state_name, county_name
        FROM cdc 
        ORDER BY state_name, county_name ASC""")
        con.commit()
    con.close()

def download_geojson():
    """Downloads the county geojson file and saves it locally
    """
    with urlopen(COUNTY_GEOJSON_URL) as response:
        counties = json.load(response)
    with open(COUNTIES_FILE,'w',encoding='utf-8') as file:
        json.dump(counties, file)

def get_counties_geojson():
    """
    Returns the county shape data in geojson format.
    Downloads the data if it is not already saved locally.
    """
    if not exists(COUNTIES_FILE):
        download_geojson()
    with open(COUNTIES_FILE,'r',encoding=str) as file:
        return json.load(file)

def get_counties_geopandas():
    """
    Returns the county shape data in geopandas format.
    """
    if not exists(COUNTIES_FILE):
        download_geojson()
    return gpd.read_file(COUNTIES_FILE)

def get_db():
    """
    Returns the object for the project database
    """
    if 'db' not in g:
        g.db = sqlite3.connect(DB_FILE, detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    """
    Closes database connection if it is open.
    """
    database = g.pop('db', None)

    if database is not None:
        database.close()

def clear_cache():
    """
    Deletes the cached dataframes for the average cases queries.
    """
    cache_dir = "cache"
    if exists(cache_dir):
        for cache_file in listdir(cache_dir):
            remove(join(cache_dir, cache_file))

if __name__ == '__main__':
    update_db()
