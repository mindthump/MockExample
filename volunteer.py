#!/usr/bin/env python

"""
Volunteer doesn't know intrinsically about the actual source of the
data, it needs to be instantiated outside and passed in.
"""

import logging

_original_author = 'ed.cardinal@wdc.com'


class Volunteer(object):
    """
    Initialization is a no-op. All the work happens inside the 'utility'
    methods.
    """

    def __init__(self):
        pass

    @staticmethod
    # For mocking, the fact that get_title_by_id is a static method is irrelevant.
    def get_title(_id, data_source, _logger):
        _name = data_source.get_title_by_id(_id)
        # Do something fancy here to justify this otherwise useless method
        fancy_title = "** {} **".format(_name)
        return fancy_title
