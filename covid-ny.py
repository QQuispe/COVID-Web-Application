import csv
import sqlite3
from urllib.request import urlopen
import pandas as pd



try:
    link = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties-2022.csv"
    df = pd.read_csv(link, index_col=0)
    
    create_table = sqlite3.connect('covid-ny.db')
    df.to_sql(name='covid-ny', con=create_table)

    create_table.commit()


except sqlite3.Error as error:
    print('Error occured - ', error)


finally:
    if create_table:
        create_table.close()
        print('Connection Closed')