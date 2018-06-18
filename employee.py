#!/usr/bin/env python

import person_data_source


class Employee(object):
    """
    Employee imports the entire person_data_source module and
    instantiates the PersonDataSource class through its namespace, then
    uses the get_name_by_id function
    """

    def __init__(self, _id):
        self.id = _id

    def name(self):
        _pds = person_data_source.PersonDataSource("db://remote_person_ds/")
        _name = _pds.get_name_by_id(self.id)
        return "#{} - {}".format(self.id, _name)
