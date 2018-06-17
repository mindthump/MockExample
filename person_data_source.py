#!/usr/bin/env python

# A placeholder for unrecognized IDs
UNKNOWN_PERSON = {'name': 'UNKNOWN', 'title': 'UNKNOWN'}


class PersonDataSource:
    """
    This is a simple representation of what could be
    a database or other source of data.
    """

    def __init__(self):
        # NOTE: This should be named something like '__people'
        # so Python treats it as pseudo-private, by renaming it to hide it.
        self.people = {
            1: {'name': 'Alice', 'title': 'Developer', 'type': 'EMPLOYEE', },
            2: {'name': 'Bob', 'title': 'Sophomore', 'type': 'STUDENT', },
            3: {'name': 'Charlie', 'title': 'Manager', },
            4: {'name': 'Darla', 'title': 'Intern', },
            5: {'name': 'Ella', 'title': 'Analyst', },
            6: {'name': 'Francis', 'title': 'QA', },
        }

    def get_name(self, person_id):
        return self.people.get(person_id, UNKNOWN_PERSON)['name']

    def get_title(self, person_id):
        return self.people.get(person_id, UNKNOWN_PERSON)['title']

    def get_person_record(self, person_id):
        return self.get_name(person_id), self.get_title(person_id)
