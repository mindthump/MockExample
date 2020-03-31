"""
This class uses the datasource 'PeopleDatabase' to fill relevant fields
on the object. It accesses the source from a number of different
contexts, so we can observe the effect of its location on mocking
activity.

'Student' imports the just the PeopleDatabase class directly from the
people_data module into this module's namespace, instantiates it and
uses the instance's get_name_by_id function. Assume for this example
it's cheap to connect but expensive to query.

Original Author: edc@mindthump.org
"""

import inspect
import logging
from people_data import PeopleDatabase

# Q1: What is the _result_ we return from the get_name_by_id() method
# if you instantiate the target of the mocking (the data source in this
# example) at the module level?
MODULE_LEVEL_PEOPLEDATABASE = PeopleDatabase("db://remote_person_ds/")
MODULE_LEVEL_PEOPLEDATABASE.connect()


class Student(object):
    def __init__(self, _id):
        self.student_id = _id
        # Q2: What if you instantiate the data source during __init__?
        self.class_level_peopledatabase = PeopleDatabase("db://remote_person_ds/")
        self.class_level_peopledatabase.connect()

    def get_badge_text(self):
        # Q3: What if you instantiate it inside the function where it's used?
        method_level_peopledatabase = PeopleDatabase("db://remote_person_ds/")
        method_level_peopledatabase.connect()

        # Get the name from each instance of the data source
        module_level_name = MODULE_LEVEL_PEOPLEDATABASE.get_name_by_id(self.student_id)
        class_level_name = self.class_level_peopledatabase.get_name_by_id(
            self.student_id
        )
        method_level_name = method_level_peopledatabase.get_name_by_id(self.student_id)
        logging.debug(
            "{} == {} == {}".format(
                module_level_name, class_level_name, method_level_name
            )
        )

        # A: In the end the results are all the same, mocked or not mocked
        assert method_level_name == class_level_name == module_level_name
        # We only really need to return one of these
        return "HI! My name is {}".format(method_level_name)
