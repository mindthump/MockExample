#!/usr/bin/env python

"""
This class uses the datasource (PeopleDatabase) to fill relevant fields
on the object. It accesses the source from a number of different
contexts, so we can observe the effect of its location on mocking activity.
Maybe this helps print name badges for a sponsored meet-up.

Student imports the PeopleDatabase class directly from the people_data
module into this module's namespace, instantiates it and uses the
instance's get_name_by_id function.
"""

from people_data import PeopleDatabase

_original_author = 'ed.cardinal@wdc.com'

# Q1: What is the _result_ we return from the name() method if you
# instantiate the target of the mocking (the data source in this
# example) at the module level?
MODULE_pds = PeopleDatabase("db://remote_person_ds/")


class Student(object):

    def __init__(self, _id):
        self.id = _id
        # Q2: What if you instantiate the data source during __init__?
        self.INSTANCE_pds = PeopleDatabase("db://remote_person_ds/")

    def get_name(self):
        # Q3: What if you instantiate it inside the function where it's used?
        METHOD_pds = PeopleDatabase("db://remote_person_ds/")

        # Get the name from each instance of the data source
        module_name = MODULE_pds.get_name_by_id(self.id)
        instance_name = self.INSTANCE_pds.get_name_by_id(self.id)
        method_name = METHOD_pds.get_name_by_id(self.id)

        # A: In the end the results are all the same: the mocked value
        assert method_name == instance_name == module_name
        # We only really need to return one of these
        return method_name
