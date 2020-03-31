"""
Employee imports the entire people_data module and
instantiates the PeopleDatabase class through its namespace, then
uses the get_name_by_id method.

Original Author: edc@mindthump.org
"""

import logging
import people_data


class Employee(object):
    _id = None

    def __init__(self, _id):
        self.employee_id = _id

    def get_badge_text(self):
        people_database = people_data.PeopleDatabase("db://remote_person_ds/")
        people_database.connect()
        employee_name = people_database.get_name_by_id(self.employee_id)
        # Decorate the name with the employee number (the ID)
        logging.debug("Employee name = {}".format(employee_name))
        return "#{} - {}".format(self.employee_id, employee_name)
