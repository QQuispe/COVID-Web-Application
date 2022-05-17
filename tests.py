import unittest
import database_query
import database_update

class Testing(unittest.TestCase):

    def test_avg_cases_table_structure(self):
        """
        Check that columns have the right names
        """
        table1 = database_query.avg_cases_table()
        self.assertEqual(list(table1.columns.values),
        ['fips_code', 'risk_level', 'state_name', 'county_name',
        'total_cases', 'total_deaths', 'cases_per_cap'])

    def test_cases(self):
        """
        Check if the database aggregation produces logically consistent results.
        There should be the same or greater number of cases in each locality over a longer time span
        """
        table1 = database_query.avg_cases_table(10)
        table2 = database_query.avg_cases_table(90)
        self.assertTrue((table1.total_cases <= table2.total_cases).all())

    def test_deaths(self):
        """
        Check if the database aggregation produces logically consistent results.
        There should be the same or greater number of deaths in each locality over a longer time span
        """
        table1 = database_query.avg_cases_table(10)
        table2 = database_query.avg_cases_table(90)
        self.assertTrue((table1.total_deaths <= table2.total_deaths).all())

    def test_cache(self):
        """
        Check if clearing the cache causes consistency errors with the tables
        """
        table1 = database_query.get_cases_table()
        database_update.clear_cache()
        table2 = database_query.get_cases_table()
        self.assertTrue(table1.equals(table2))

    

if __name__ == '__main__':
    unittest.main()
