import csv
import sqlite3



try:

    with open('us-counties.csv', 'r') as covid:
        data = csv.DictReader(covid)
        ny_data = [(i['date'], i['county'], i['state'], i['fips'], i['cases'], i['deaths']) for i in data]

    create_table = sqlite3.connect('covid-ny.db')
    cursor = create_table.cursor()
    cursor.execute('create table NYData(date, county, state, fips, cases, deaths);')
    cursor.executemany("insert into NYData (date,county,state,fips,cases,deaths) VALUES(?,?,?,?,?,?);", ny_data)
    cursor.execute('select * from NYData;')
    create_table.commit()

    result = cursor.fetchall()
    print(result)


except sqlite3.Error as error:
    print('Error occured - ', error)


finally:
    if create_table:
        create_table.close()
        print('Connection Closed')