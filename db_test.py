# Move all code from exploration_and_cleaning.ipynb into a function to use with map.py

# import the folium library
import folium
import sqlite3
import pandas as pd

def exploration_and_cleaning():
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
    cases_df = cases_df.sort_values(by = ['cases'])

    cases_df = cases_df.sort_values(by = ['test_percent'])

    #change None to zero
    cases_df.test_percent.fillna("0", inplace = True)
    #remove commas
    cases_df.test_percent = cases_df.test_percent.apply(lambda x: x.replace(',',''))
    #now test percent can be converted to a numeric data type
    cases_df.test_percent = cases_df.test_percent.astype(float)
    cases_df = cases_df.sort_values(by = ['test_percent'])

    plot_df = cases_df.copy()
    plot_df = plot_df.groupby('fips_code').agg({'cases' : 'mean'}).reset_index()

    from urllib.request import urlopen
    import json
    with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
        counties = json.load(response)

    plot_df = cases_df.copy()
    plot_df = plot_df.groupby('fips_code').agg({'cases' : 'mean'}).reset_index()
    plot_df['STATE'] = plot_df.fips_code.apply(lambda x: x[0:2])
    plot_df['County'] = plot_df.fips_code.apply(lambda x: x[2:5])

    # initialize the map and store it in a m object
    m = folium.Map(location=[40, -95], zoom_start=4)

    folium.Choropleth(
        geo_data=counties,
        name="choropleth",
        data=plot_df,
        columns=["fips_code", "cases"],
        key_on="feature.id",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=.1,
        legend_name="Cases per 100K average",
    ).add_to(m)

    folium.LayerControl().add_to(m)

    return m