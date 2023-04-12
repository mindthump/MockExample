#!/usr/bin/env python

"""
Print decorated name badges from DB. It's pretty stupid, but good enough
to demonstrate the mocking techniques. I have no plans to improve it...

Original Author: edc@mindthump.org
"""
import sys
import argparse
from people.people_data import PeopleData
from people import student, employee, utils
from people.volunteer import Volunteer


class BadgeApp(object):
    """ """

    def __init__(self, init_parameters):
        """ """
        parser = argparse.ArgumentParser(description="Print name badges.")
        parser.add_argument(
            "-v",
            "--verbose",
            help="Show all log messages on standard error stream",
            action="store_true",
        )
        self.args = parser.parse_args(init_parameters)
        self.peopleDatabase = PeopleData()
        PeopleData.initialize_db()

    def run(self):
        """ """
        students = self.peopleDatabase.get_people_by_type("STUDENT")
        print("------- STUDENTS -------")
        for student_ in students:
            print(student.Student(student_[0]).get_badge_text())

        employees = self.peopleDatabase.get_people_by_type("EMPLOYEE")
        print("------- EMPLOYEES -------")
        for employee_ in employees:
            print(employee.Employee(employee_[0]).get_badge_text())

        volunteers = self.peopleDatabase.get_people_by_type("VOLUNTEER")
        print("------- VOLUNTEERS -------")
        for volunteer_ in volunteers:
            print(Volunteer().get_badge_text(volunteer_[0], self.peopleDatabase))

        return 0


if __name__ == "__main__":
    # Setup and run the application.
    utils.initialize_logging()
    result = BadgeApp(sys.argv[1:]).run()
    sys.exit(result)
