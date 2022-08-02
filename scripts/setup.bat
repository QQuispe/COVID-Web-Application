@echo off
echo Creating virtual environment
py -m venv venv
call venv\Scripts\activate
pip install flask
pip install pandas
pip install folium
pip install branca
pip install sodapy
pip install missing_packages/GDAL-3.4.2-cp310-cp310-win_amd64.whl
pip install missing_packages/Fiona-1.8.21-cp310-cp310-win_amd64.whl
pip install geopandas
echo Finished setting up the virtual environment
echo Setting up the database. This may take several minutes
call update.bat
echo Database update complete
call run.bat