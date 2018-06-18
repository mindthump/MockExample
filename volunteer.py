#!/usr/bin/env python

import people_data


class Volunteer(object):
    """
    """

    def __init__(self, _id):
        self.id = _id

    def name(self):
        _pds = people_data.PeopleDatabase("db://remote_person_ds/")
        _name = _pds.get_name_by_id(self.id)
        return _name
