#!/usr/bin/env python

"""
Wrapper around sqlite3 database

This module isn't a mock! It is a "test double", essentially a
simulator. This will be the _target_ of our mocking. There are both
basic functions/methods that return a value, and a more general query
returning an iterable of data structures (rows, JSON, etc.)

Original Author: edc@mindthump.com
"""

import sqlite3
import logging

# TODO: Maybe wait a while here and there to show "cost" savings ;)

# Fake data to fill our fake database.
people_test_data = [(1, 'Alice', 'Developer', 'EMPLOYEE',),
    (2, 'Brenda', 'Sophomore', 'STUDENT',), (3, 'Charlie', 'Manager', 'EMPLOYEE',),
    (4, 'Darla', 'Intern', 'VOLUNTEER',), (5, 'Ella', 'Analyst', 'EMPLOYEE',),
    (6, 'Francis', 'QA', 'EMPLOYEE',), (7, 'George', 'Freshman', 'STUDENT',),
    (8, 'Harvey', 'Slave', "VOLUNTEER")]


class PeopleDatabase(object):
    _db = None
    db_connect_string = None

    def __init__(self, _db_connect_string):
        self.db_connect_string = _db_connect_string

    def connect(self):
        """
        Create the temporary database and fill it.
        """
        self._db = sqlite3.connect(":memory:")
        self._db.execute("CREATE TABLE people(id INT, name TEXT, title TEXT, type TEXT)")
        self._db.executemany(
            "INSERT INTO people (id, name, title, type) VALUES (?, ?, ?, ?)",
            people_test_data)
        logging.debug("Database initialized.")

    def _query(self, query_string):
        raw_query_cursor = self._db.execute(query_string)
        result = raw_query_cursor.fetchall()
        if not result:
            raise self._db.DataError(
                "No matching results found in database for query: '{}'".format(
                    query_string))
        logging.debug("Completed query, returning results.")
        return result

    def get_name_by_id(self, query_id):
        """
        This is the primary method we will patch.
        The presumption is that going out to the real resource is an "expensive"
        operation (time, money, network, etc.), not suitable in a unit test.
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
        result = self._query("SELECT * FROM people WHERE type = '{}'".format(query_type))
        logging.debug("Completed get_all_people.")
        return result
