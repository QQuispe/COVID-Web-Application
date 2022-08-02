#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
echo Creating Virural environment
python3 -m venv venv ../
source venv/bin/activate
pip install flask
pip install pandas
pip install folium
pip install branca
pip install sodapy
pip install geopandas
pip install python-dotenv
echo Finished setting up the virtual environment
source "$DIR/update.sh"
source "$DIR/run.sh"