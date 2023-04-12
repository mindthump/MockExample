"""
This class is a wrapper around an in-memory sqlite3 database. The
database represents a resource that lives "out there somewhere".

This class will be the _target_ of our mocking. There are basic
functions/methods that return a value, and more general queries
returning iterables of data structures (rows, JSON, etc.)

IMPORTANT: For simplicity in our example, clients access specific
columns in results by number. If needed we could get the column names
from the query's `description` attribute.

And there is no error checking at all -- this is just an example!

Original Author: edc@mindthump.org
"""

import sqlite3
import logging
import time


# Data to fill our test database.
people_test_data = [
    (1, "Alice", "Developer", "EMPLOYEE"),
    (2, "Brenda", "Senior at Cal", "STUDENT"),
    (3, "Charlie", "Manager", "EMPLOYEE"),
    (4, "Darla", "Intern", "VOLUNTEER"),
    (5, "Ella", "Analyst", "EMPLOYEE"),
    (6, "Francis", "QA", "EMPLOYEE"),
    (7, "George", "Freshman at Stanford", "STUDENT"),
    (8, "Harvey", "Charlie's Friend", "VOLUNTEER"),
]


class PeopleData(object):
    """
    """
    # Class variable; each call to `connect()` for an in-memory DB is a new instance
    connection = sqlite3.connect(":memory:")

    @classmethod
    def initialize_db(cls):
        """
        Fill the database with data from the list of tuples above.
        """
        cls.connection.execute(
            "CREATE TABLE people(id INT, name TEXT, title TEXT, type TEXT)"
        )
        cls.connection.executemany(
            "INSERT INTO people (id, name, title, type) VALUES (?, ?, ?, ?)",
            people_test_data,
        )
        logging.debug("Database initialized.")

    def _query(self, query_string):
        """
        A generic method to get all the returned rows to a list, catch some errors,
        do some logging, and sit around doing nothing for a short time to represent an
        "expensive" resource.
        """
        # Wait a while here to show "cost" ;)
        time.sleep(2)
        raw_query_cursor = self.connection.execute(query_string)
        result = raw_query_cursor.fetchall()
        # We're raising this error on purpose, to investigate `pytest.raises()`
        if not result:
            raise self.connection.DataError(
                "No matching results found in database for query: '{}'".format(
                    query_string
                )
            )
        logging.debug("Completed query, returning results.")
        return result

    def get_name_by_id(self, query_id):
        """
        This is the primary method we will patch. There is nothing
        special here to accommodate tests, it's just ordinary code; that
        is the true beauty of the mocking techniques.
        """
        result = self._query("SELECT name FROM people WHERE id = {}".format(query_id))
        # There should be :) only one value in one record.
        logging.debug("Completed get_name_by_id.")
        return result[0][0]

    def get_title_by_id(self, query_id):
        result = self._query("SELECT title FROM people WHERE id = {}".format(query_id))
        logging.debug("Completed get_title_by_id.")
        return result[0][0]

    def get_all_people(self):
        result = self._query("SELECT * FROM people")
        logging.debug("Completed get_all_people.")
        return result

    def get_people_by_type(self, query_type):
        result = self._query(
            "SELECT * FROM people WHERE type = '{}'".format(query_type)
        )
        logging.debug("Completed get_people_by_type.")
        return result
