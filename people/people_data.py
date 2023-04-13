"""

This class is a wrapper around an in-memory sqlite3 database. It
represents a resource that lives "out there somewhere".

This class will be the _target_ of our mocking. There are basic
functions/methods that return a value, and more general queries
returning iterables of data structures (rows, JSON, etc.)

IMPORTANT: For simplicity in our example, clients access specific
columns in results by number. If needed we could get the column names
from the query's `description` attribute.

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
    """ """

    # Class variable; each call to `connect()` for sqlite3 in-memory is a new instance
    connection = sqlite3.connect(":memory:")

    @classmethod
    def initialize_data(cls):
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

    def _query(self, query_string, parameters=None):
        """
        A generic method to get all the returned rows to a list, catch some errors,
        do some logging, and sit around doing nothing for a short time to represent an
        "expensive" resource.
        """
        # Wait a while here to show "cost" ;)
        time.sleep(2)
        if parameters:
            raw_query_cursor = self.connection.execute(query_string, parameters)
        else:
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

    # TODO: Call this on object initialization?
    def get_person_by_id(self, query_id):
        """
        This is the primary method we will patch. There is nothing
        special here to accommodate tests, it's just ordinary code; that
        is the true beauty of the mocking techniques.
        """
        result = self._query("SELECT * FROM people WHERE id = ?", [query_id])
        logging.debug(f"Completed get_person_by_id: {result}.")
        # There should be :) only one record.
        return result[0]

    # TODO: A property of the type?
    def get_name_by_id(self, query_id):
        """
        A utility method to extract one field.
        """
        result = self.get_person_by_id(query_id)[1]
        logging.debug(f"Completed get_name_by_id: {query_id} => {result}.")
        return result

    def get_title_by_id(self, query_id):
        result = self.get_person_by_id(query_id)[2]
        logging.debug(f"Completed get_title_by_id: {query_id} => {result}.")
        return result

    def get_all_people(self):
        result = self._query("SELECT * FROM people")
        logging.debug(f"Completed get_all_people, returned {len(result)} rows.")
        return result

    def get_people_by_type(self, query_type):
        result = self._query("SELECT * FROM people WHERE type = ?", [query_type])
        logging.debug(
            f"Completed get_people_by_type for '{query_type}', returned {len(result)} rows."
        )
        return result
