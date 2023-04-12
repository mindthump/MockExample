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
        employee_data = people_data.PeopleData()
        employee_name = employee_data.get_name_by_id(self.employee_id)
        # Decorate the name with the employee number (the ID)
        logging.debug("Employee name = {}".format(employee_name))
        return "#{} - {}".format(self.employee_id, employee_name)
