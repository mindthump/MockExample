#!/usr/bin/env python

import person_data_source


class Volunteer(object):
    """
    """

    def __init__(self, _id):
        self.id = _id

    def name(self):
        _pds = person_data_source.PersonDataSource()
        _name = _pds.get_name(self.id)
        return _name
