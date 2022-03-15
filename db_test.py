import folium
import sqlite3
import pandas as pd
from database_update import get_counties_geojson

def make_map():
    con = sqlite3.connect("covid.sqlite")
    cur = con.cursor()

    plot_df = pd.read_sql_query("""SELECT state_name, county_name, fips_code, avg(replace(replace(cases_per_100k_7_day_count,'suppressed','0'),',','')) as cases 
    FROM cases 
    WHERE date >= DATE('now','-31 day')
    GROUP BY fips_code""", con)

    #TODO determine cutoff programatically rather than hardcoded 500
    plot_df['plot_cases'] = plot_df.cases.map(lambda x: min(x,500))

    counties = get_counties_geojson()
    
    # initialize the map and store it in a m object
    

    m = folium.Map(location=[40, -95], zoom_start=4,tiles = None)

    folium.Choropleth(
        geo_data=counties,
        name="Covid Cases",
        data=plot_df,
        columns=["fips_code", "plot_cases"],
        key_on="feature.id",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=1,
        legend_name="Weekly Cases per 100K"
        ).add_to(m)

    folium.LayerControl().add_to(m)

    return m