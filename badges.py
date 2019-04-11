# from __future__ import print_function
"""
Print decorated name badges from DB.
Yes, it repeatedly bangs on the same DB.
It's pretty stupid, but bear with it...

Original Author: edc@mindthump.org
"""
import utils
import sys
import argparse
from people_data import PeopleDatabase
import student
import employee
import volunteer


class BadgeApp(object):
    """
    """

    def __init__(self, init_parameters):
        """
        """
        parser = argparse.ArgumentParser(description='Print name badges.')
        parser.add_argument('-v', '--verbose',
            help='Show all log messages on standard error stream', action='store_true')
        self.args = parser.parse_args(init_parameters)
        self.peopledatabase = None

    def init_people_database(self):
        """
        """
        self.peopledatabase = PeopleDatabase("db://remote_person_ds/")
        self.peopledatabase.connect()

    def run(self):
        """
        """
        self.init_people_database()
        # people = self.peopledatabase.get_all_people()
        students = self.peopledatabase.get_people_by_type('STUDENT')
        for _student in students:
            print(student.Student(_student[0]).get_badge_text())

        employees = self.peopledatabase.get_people_by_type('EMPLOYEE')
        for _employee in employees:
            print(employee.Employee(_employee[0]).get_badge_text())

        volunteers = self.peopledatabase.get_people_by_type('VOLUNTEER')
        for _volunteer in volunteers:
            print(volunteer.Volunteer().get_badge_text(_volunteer[0], self.peopledatabase))

        return 0


if __name__ == "__main__":
    # Setup and run the application.
    utils.initialize_logging()
    result = BadgeApp(sys.argv[1:]).run()
    sys.exit(result)
