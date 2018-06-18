#!/usr/bin/env python

from attr import attrs, attrib
import person_data_source


@attrs
class Volunteer(object):
    """
    """
    name = attrib()

    def __init__(self, _id):
        self.id = _id

    def name(self):
        _pds = person_data_source.PersonDataSource("db://remote_person_ds/")
        _name = _pds.get_name_by_id(self.id)
        return _name
