#!/usr/bin/env python

"""
This module isn't a mock! It is a "test double", essentially a
simulator. This will be the target of our mocking. It could represent a
database, a server, a REST API, or other source of data. There are both
basic functions/methods that return a value, and a more general query
returning an iterable of data structures (rows, JSON, etc.)

The presumption is that this is an "expensive" operation (time, money,
network, etc.), not suitable in a unit test.

TODO: Maybe wait a while here and there to show cost savings  ;)

"""

# A placeholder for unrecognized IDs
UNKNOWN_PERSON = {'name': 'UNKNOWN', 'title': 'UNKNOWN'}


# noinspection PyUnusedLocal
class PersonDataSource:

    def __init__(self, _datasource_connection_string):
        """
        Passing in the connection string makes it easier to mock
        connect() method. If we hold it on the object then read it
        inside a method we can't "reach inside" the method to alter the
        value at runtime by mocking
        TODO: reach inside a method to alter a variable value? Doubtful!
        """
        # FIXME: This should be named something like '__people'
        # so Python treats it as pseudo-private, by renaming it to hide it.
        self.people = None
        # self.datasource_connection_string = datasource_connection_string
        self.connect(_datasource_connection_string)

    def connect(self, _datasource_connection_string):
        # Ignore the connection string (for now)
        self.people = {
            1: {'name': 'Alice', 'title': 'Developer', 'type': 'EMPLOYEE', },
            2: {'name': 'Brenda', 'title': 'Sophomore', 'type': 'STUDENT', },
            3: {'name': 'Charlie', 'title': 'Manager', 'type': 'EMPLOYEE', },
            4: {'name': 'Darla', 'title': 'Intern', 'type': 'VOLUNTEER', },
            5: {'name': 'Ella', 'title': 'Analyst', 'type': 'EMPLOYEE', },
            6: {'name': 'Francis', 'title': 'QA', 'type': 'EMPLOYEE', },
            7: {'name': 'George', 'title': 'Freshman', 'type': 'STUDENT', },
        }
        return

    def get_name_by_id(self, person_id):
        return self.get_record_by_id(person_id)['name']

    def get_title_by_id(self, person_id):
        return self.get_record_by_id(person_id)['title']

    def get_record_by_id(self, person_id):
        return self.people.get(person_id, UNKNOWN_PERSON)

    def query(self, query_string):
        """
        Generator of fake 'rows'.
        TODO: Use the query string to filter rows? Demo mocking the query?
        """
        for person in self.people:
            yield person
