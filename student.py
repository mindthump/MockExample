#!/usr/bin/env python

from person_data_source import PersonDataSource

# Q: What if you instantiate the target of the mocking (the data source in this example)
# at the module level?
module_pds = PersonDataSource()


class Student(object):
    """
    Student imports the PersonDataSource class directly from the
    person_data_source module into this module's namespace, instantiates it and
    uses the instance's get_name function. This also means we don't have
    direct access at the test level to anything at the data source's
    module level (like UNKNOWN_PERSON).
    """

    def __init__(self, _id):
        self.id = _id
        # Q: What if you instantiate the data source during __init__?
        self.instance_pds = PersonDataSource()

    def name(self):
        # Q: What if you instantiate it inside the function where it's used?
        _pds = PersonDataSource()
        module_name = module_pds.get_name(self.id)
        instance_name = self.instance_pds.get_name(self.id)
        _name = _pds.get_name(self.id)
        # A: In the end the values are all the same: the mocked value
        assert _name == instance_name == module_name
        return _name
