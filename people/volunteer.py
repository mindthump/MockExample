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
    # For mocking, the fact that get_title_by_id is a
    # classmethod (or staticmethod) is irrelevant. What is important is
    # where it is located in the code. (Technically, the
    # namespace... but don't worry about that.)
    def get_badge_text(cls, _id, people_data):
        volunteer_title = people_data.get_title_by_id(_id)
        volunteer_name = people_data.get_name_by_id(_id)
        return f"** {volunteer_name} ({volunteer_title}) **"
