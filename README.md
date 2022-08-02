# COVID-Web-Application

## Intro
This Flask web application displays COVID-19 data in the United States. It combines data from the CDC and New York Times to display data at a county-level.

***

## Getting started

``` Bash
# clone project
git clone https://github.com/QQuispe/COVID-Web-Application
cd COVID-Web-Application
```

## Configuration

This app uses python-dotenv for environment variables. In order to run the web app you will need to get a Socrata API Token. Grab one [here](https://evergreen.data.socrata.com/) and set up your token in your ```.env``` file. A sample .env file is also provided.

 ```
 SOCRATA = "YOUR_TOKEN"
 ```

## Starting the web application

 ``` bash
# run setup script
bash script/setup.sh
```
Running the setup script will install dependencies, run other setup files, and launch the web app.

***

## Scripts

Use ```setup.sh``` when running the project for the first time as it will set up everything for you.
 ``` bash
# run setup script
bash script/setup.sh
```
Use ```update.sh``` when you only need to update the database.
 ``` bash
# run update script
bash script/update.sh
```
Use ```run.sh``` to launch the web app.
 ``` bash
# run start script
bash script/run.sh
```

***

## Recognitions
This project was made in collaboration with Mike, Devon, Raf, and Dennis.