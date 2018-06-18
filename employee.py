#!/usr/bin/env python

import people_data


class Employee(object):
    """
    Employee imports the entire person_data_source module and
    instantiates the PeopleDatabase class through its namespace, then
    uses the get_name_by_id function
    """

    def __init__(self, _id):
        self.id = _id

    def name(self):
        _pds = people_data.PeopleDatabase("db://remote_person_ds/")
        _name = _pds.get_name_by_id(self.id)
        return "#{} - {}".format(self.id, _name)
