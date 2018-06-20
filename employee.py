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

    def __init__(self, _id, _logger):
        self.id = _id
        self.logger = logging.getLogger(__name__)
        pass

    def get_name(self):
        _pds = people_data.PeopleDatabase("db://remote_person_ds/")
        _name = _pds.get_name_by_id(self.id)
        # Decorate the name with the employee number (the ID)
        return "#{} - {}".format(self.id, _name)
