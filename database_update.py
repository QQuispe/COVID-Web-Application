import sqlite3
import pandas as pd
from sodapy import Socrata

data_addr = "https://data.cdc.gov/resource/nra9-vzzn.json"


data_url='data.cdc.gov'    # The Host Name for the API endpoint
cases_data_set='nra9-vzzn' # Covid Cases data set
vaccinations_data_set='8xkx-amqh' # Covid vaccinations dataset

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