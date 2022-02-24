from cmath import inf
import sqlite3
import pandas as pd
from sodapy import Socrata

data_addr = "https://data.cdc.gov/resource/nra9-vzzn.json"


data_url='data.cdc.gov'    # The Host Name for the API endpoint
cases_data_set='nra9-vzzn' # Covid Cases data set
vaccinations_data_set='8xkx-amqh' # Covid vaccinations dataset

# Read Socrata API key from key.txt
with open('key.txt') as f:
    app_token = f.read()

client = Socrata(data_url, app_token)      # Create the client to point to the API endpoint
# Set the timeout to 4 minutes
client.timeout = 240

# Setting an excessively high limit to make sure all records are retrieved
# TODO change this query to only retrieve new records
results = client.get(cases_data_set, limit = 100000000)
# Convert the list of dictionaries to a Pandas data frame
covid_df = pd.DataFrame.from_records(results)

#open connection to the database
con = sqlite3.connect("covid.sqlite")
covid_df.to_sql("cases", con, if_exists="replace")
con.close()