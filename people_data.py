#!/usr/bin/env python

import sqlite3

"""
Wrapper around sqlite3 database

This module isn't a mock! It is a "test double", essentially a
simulator. This will be the _target_ of our mocking. There are both
basic functions/methods that return a value, and a more general query
returning an iterable of data structures (rows, JSON, etc.)

The presumption is that this is an "expensive" operation (time, money,
network, etc.), not suitable in a unit test.
"""

# TODO: Maybe wait a while here and there to show "cost" savings ;)

people_data = [
    (1, 'Alice', 'Developer', 'EMPLOYEE',),
    (2, 'Brenda', 'Sophomore', 'STUDENT',),
    (3, 'Charlie', 'Manager', 'EMPLOYEE',),
    (4, 'Darla', 'Intern', 'VOLUNTEER',),
    (5, 'Ella', 'Analyst', 'EMPLOYEE',),
    (6, 'Francis', 'QA', 'EMPLOYEE',),
    (7, 'George', 'Freshman', 'STUDENT',),
]


class PeopleDatabase:
    _db = None

    def __init__(self, db_connect_string):
        self.db_connect_string = db_connect_string
        self._db = sqlite3.connect(":memory:")
        self._db.execute("""CREATE TABLE people(id INT, name TEXT, title TEXT, type TEXT)""")
        self._db.executemany("""INSERT INTO people (id, name, title, type) VALUES (?, ?, ?, ?)""", people_data)
        pass

    def query(self, query_string):
        raw_query_cursor = self._db.execute(query_string)
        # Returns something that acts like a list of tuples
        result = raw_query_cursor.fetchall()
        if not result:
            raise self._db.DataError("No matching results found in database for query: '{}'".format(query_string))
        return result

    def get_name_by_id(self, query_id):
        result = self.query("SELECT name FROM people WHERE id = {}".format(query_id))
        return result[0][0]

    def get_title_by_id(self, query_id):
        result = self.query("SELECT title FROM people WHERE id = {}".format(query_id))
        return result[0][0]
