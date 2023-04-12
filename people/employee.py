"""
Employee imports the entire people_data module and
instantiates the PeopleData class through its namespace, then
uses the get_name_by_id method.

Original Author: edc@mindthump.org
"""

import logging
from people import people_data


class Employee(object):
    _id = None

    def __init__(self, _id):
        self.employee_id = _id

    def get_badge_text(self):
        employee_data = people_data.PeopleData().get_person_by_id(self.employee_id)
        employee_name = employee_data[1]
        employee_title = employee_data[2]
        # Decorate the name with the employee number (the ID)
        logging.debug(f"Employee name = {employee_name}")
        return f"#{self.employee_id} - {employee_name} ({employee_title})"
