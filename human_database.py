#!/usr/bin/env python

import sqlite3

"""
Wrapper around sqlite3 database
"""

people_data = [
    (1, 'Alice', 'Developer', 'EMPLOYEE',),
    (2, 'Brenda', 'Sophomore', 'STUDENT',),
    (3, 'Charlie', 'Manager', 'EMPLOYEE',),
    (4, 'Darla', 'Intern', 'VOLUNTEER',),
    (5, 'Ella', 'Analyst', 'EMPLOYEE',),
    (6, 'Francis', 'QA', 'EMPLOYEE',),
    (7, 'George', 'Freshman', 'STUDENT',),
]


class HumanDatabase:
    _db = None

    def __init__(self):
        self._db = sqlite3.connect(":memory:")
        self._db.execute("""CREATE TABLE people(id INT, name TEXT, title TEXT, type TEXT)""")
        self.fill_db()
        pass

    def fill_db(self):
        self._db.executemany("""INSERT INTO people (id, name, title, type) VALUES (?, ?, ?, ?)""", people_data)
        pass

    def get_name_by_id(self, query_id):
        result = self.query("SELECT name FROM people WHERE id = {}".format(query_id))
        return result.fetchone()[0]

    def query(self, query_string):
        result = self._db.execute(query_string)
        return result
