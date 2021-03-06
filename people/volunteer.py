"""
Volunteer doesn't know intrinsically about the actual source of the
data, it needs to be instantiated outside and passed in.

Original Author: edc@mindthump.org
"""

import logging


class Volunteer(object):
    """
    Initialization is a no-op. All the work happens inside the 'utility'
    methods.
    """

    def __init__(self):
        pass

    @classmethod
    # For mocking, the fact that get_title_by_id is a static method is irrelevant.
    def get_badge_text(cls, _id, data_source):
        _title = data_source.get_title_by_id(_id)
        return "** {} **".format(_title)
