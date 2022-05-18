call venv\Scripts\activate
set FLASK_APP=covid_app
start "" flask run
start "" http://127.0.0.1:5000/
