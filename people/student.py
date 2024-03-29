"""
This class uses the datasource 'PeopleData' to fill relevant fields
on the object.

'Student' imports the PeopleData class directly from the
people_data module into this module's namespace, instantiates it and
uses the instance's get_name_by_id function.

Original Author: edc@mindthump.org
"""

import logging
from people.people_data import PeopleData


class Student(object):
    def __init__(self, _id):
        self.student_id = _id

    def get_badge_text(self):
        people_data = PeopleData()

        # Get the name from each instance of the data source
        student_name = people_data.get_name_by_id(self.student_id)
        student_title = people_data.get_title_by_id(self.student_id)
        logging.debug(f"name: {student_name}, title: {student_title}")

        return f"HI! My name is {student_name} ({student_title})"
