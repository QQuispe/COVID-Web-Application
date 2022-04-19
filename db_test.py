import folium
import branca
from database_update import get_counties_geopandas
from database_query import avg_cases_table

def make_map(days = 30):
    plot_df = avg_cases_table(days)  
    counties = get_counties_geopandas()
    counties = counties.merge(plot_df, left_on = "id", right_on = "fips_code",how = "inner")

    counties["rounded_cases"] = counties["cases"].map(lambda x: round(x,1))

    # initialize a blank map
    m = folium.Map(location=[40, -95], zoom_start=4,tiles = None)

    #maps a case count to a color
    #.95 upper quantile to avoid outliers throwing off the color scale
    colormap = branca.colormap.LinearColormap(
        vmin=plot_df["cases"].quantile(0.0),
        vmax=plot_df["cases"].quantile(.95),
        colors=['#ffffb2','#fecc5c','#fd8d3c','#f03b20','#bd0026'],#colorscale from color brewer: https://colorbrewer2.org/#type=sequential&scheme=YlOrRd&n=5
        caption = "Weekly Cases per 100K"
    )

    #styling function used by folium's geojson map
    #fills each county with a color representative of its covid case rate
    def style_func(x):
        cases = x["properties"]["cases"]
        return {"weight": .3,#seems to provide the right sized border between counties
        "fillColor": colormap(cases)
        if cases is not None
        else "transparent",
        "color": "black",
        "fillOpacity": 0.7,
        }

    #Hover over tooltip that displays county names and cases.
    hover = folium.GeoJsonTooltip(
        fields=["county_name", "state_name", "rounded_cases"],
        aliases=["Locality:", "State:", "Weekly Cases Per 100K:"],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 1px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
        )

    #popup that displays data when a county is clicked on
    #this displays the same data as the hover tooltip
    click = folium.GeoJsonPopup(
        fields=["county_name", "state_name", "rounded_cases"],
        aliases=["Locality:", "State:", "Weekly Cases Per 100K:"],
        localize=True,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 1px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
        )
    
    #with the styling function, this mirrors the appearance and functionality of the choropleth map
    g = folium.GeoJson(
        counties,
        name = "Covid Cases",
        style_function=style_func,    
        tooltip=hover,
        popup=click,
    ).add_to(m)

    #useful if additional layers are added later. no purpose to have it unless there are multiple selectable layers
    #will be useful if we want to add state level data to the map.
    #folium.LayerControl().add_to(m)

    return m
