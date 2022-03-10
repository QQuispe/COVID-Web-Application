from flask import Flask, flash, render_template
from db_test import *
import folium

app = Flask(__name__)

# Load home page
@app.route('/')
def index():
    return render_template('home.html')

# Test page currently displays a default map
@app.route('/map1')
def map1():
    start_coords = (39.089557, -77.184127)
    map = folium.Map(location=start_coords, zoom_start=14)
    return map._repr_html_()

# Test page currently displays only a map from db_test.py which is the data from exploration_and_cleaning.ipynb
@app.route('/map2')
def map2():
    return exploration_and_cleaning()._repr_html_()

# Test page with form and map
@app.route('/map3')
def map3():
    map = exploration_and_cleaning()
    return render_template('map_test.html', map=map._repr_html_())

if __name__ == '__main__':
    app.run(debug=True)