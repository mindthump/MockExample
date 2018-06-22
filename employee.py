#!/usr/bin/env python

"""
Employee imports the entire people_data module and
instantiates the PeopleDatabase class through its namespace, then
uses the get_name_by_id method.
"""

import logging
import people_data

_original_author = 'ed.cardinal@wdc.com'


class Employee(object):
    _id = None

    def __init__(self, _id):
        self.id = _id

    def get_badge_text(self):
        _pds = people_data.PeopleDatabase("db://remote_person_ds/")
        _pds.connect()
        _name = _pds.get_name_by_id(self.id)
        # Decorate the name with the employee number (the ID)
        logging.debug("Employee name = {}".format(_name))
        return "#{} - {}".format(self.id, _name)
