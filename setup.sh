#!/bin/shell
echo Creating Virural environment
python3 -m venv venv
source venv/bin/activate
#pip install flask
#pip install pandas
#pip install folium
#pip install branca
#pip install sodapy
#pip install geopandas
echo finished the virtual environment 
#source update.sh
echo setting up the database
source run.sh
