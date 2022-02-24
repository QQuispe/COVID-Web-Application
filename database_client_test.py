import sqlite3
import pandas as pd

con = sqlite3.connect("covid.sqlite")
cur = con.cursor()

cur.execute('SELECT * FROM covid')
data = cur.fetchall()
print(data[-1])


covid_df = pd.read_sql_query('SELECT * FROM covid WHERE state_name = "Maryland"', con)
print(max(covid_df.index))
print(covid_df.head(10))
con.close()