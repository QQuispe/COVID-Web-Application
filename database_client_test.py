import sqlite3
import pandas as pd

con = sqlite3.connect("covid.sqlite")
cur = con.cursor()

covid_df = pd.read_sql_query('SELECT * FROM cases WHERE state_name = "Texas" ORDER BY date DESC', con)
print("Texas covid cases test:")
print(covid_df.sort_values(by=['cases_per_100k_7_day_count']))

vax_df = pd.read_sql_query('SELECT * FROM vaccinations WHERE recip_state = "MD"', con)
print("MD covid vaccinations test:")
print(vax_df.head(10))
con.close()