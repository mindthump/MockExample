#!/usr/bin/env python

"""
Examples of mocking techniques, with minimal comments

Original Author: edc@mindthump.org
"""

import pytest
from mock import patch, MagicMock
import logging
import utils
import employee  # the entire module
from student import Student  # a specific class
import volunteer
import people_data

utils.initialize_logging()

_original_author = "edc@mindthump.org"


# Target imports class
@patch("student.PeopleDatabase.get_name_by_id")
def test_student(mock_student_getname):
    mock_student_getname.return_value = "Sam"
    student_two = Student(2)
    student_two_name = student_two.get_badge_text()
    logging.info("Student #2 name = '{}'".format(student_two_name))
    assert student_two_name == "HI! My name is Sam"


# Target imports module
@patch("employee.people_data.PeopleDatabase.get_name_by_id")
def test_employee(mock_employee_getname):
    mock_employee_getname.return_value = "Bob"
    employee_name = employee.Employee(1).get_badge_text()
    logging.warning("Employee #1 = '{}'".format(employee_name))
    assert employee_name == "#1 - Bob"


# Pass mock object as argument
def test_volunteer():
    _pds = people_data.PeopleDatabase("db://remote_person_ds/")
    _pds.connect()
    title = volunteer.Volunteer.get_badge_text(4, _pds)
    assert title == "** Intern **"
    mock_database = MagicMock()
    mock_database.get_title_by_id.return_value = "Slave"
    title = volunteer.Volunteer.get_badge_text(4, mock_database)
    assert title == "** Slave **"


# Patch as context manager
def test_context_manager():
    # Not patched
    unpatched_employee = employee.Employee(1).get_badge_text()
    assert unpatched_employee == "#1 - Alice"

    with patch(
        "employee.people_data.PeopleDatabase.get_name_by_id"
    ) as mock_employee_getname:
        mock_employee_getname.side_effect = ["Bob", "Tom"]
        patched_employee = employee.Employee(16)
        employee_name = patched_employee.get_badge_text()
        assert employee_name == "#16 - Bob"
        second_patched_employee = employee.Employee(105)
        employee_name = second_patched_employee.get_badge_text()
        assert employee_name == "#105 - Tom"
        assert mock_employee_getname.call_count == 2


# Patch entire class
@patch("employee.people_data.PeopleDatabase")
def test_class_patch(mock_datasource_class):
    mock_datasource_class.return_value.get_name_by_id.return_value = "Bob"
    employee_name = employee.Employee(1).get_badge_text()
    assert employee_name == "#1 - Bob"


# Test call raises exception
def test_raises_exception():
    humans = people_data.PeopleDatabase("db://remote_person_ds/")
    humans.connect()
    with pytest.raises(people_data.sqlite3.DataError):
        humans.get_name_by_id(120)
