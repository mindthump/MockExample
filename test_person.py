#!/usr/bin/env python

import pytest
import pprint
from mock import patch
import employee  # the entire module
from student import Student  # a specific class
import human_database

"""
The whole point of mocking is to monitor and/or alter the __behavior__ of running
objects **without changing the original code**.
Patch as "small" as you can; whenever possible only the specific behavior that is 
actually __used__.
Exception: if a resource class is expensive or impossible to instantiate you may need 
to patch the whole class.
"""


@patch('student.PersonDataSource.get_name_by_id')
def test_student_name(mock_student_datasource_getname):
    """
    A single method is the simplest to patch. The student.py module
    imports PersonDataSource directly so that's what we call it. The
    tricky part is knowing its name inside the running code; 'import'
    statements are a good clue.
    """

    # Set the value our mock object will return for the mocked
    # get_name_by_id() function The id argument is immaterial - since
    # we override the return value, the input doesn't go anywhere.
    # "Sam" never appears in the data, so it also acts as a guard from
    # accidental false-positive tests.
    mock_student_datasource_getname.return_value = "Sam"
    # NOTE: If we use side_effect() instead we can make use of
    # arguments; see mock_employee_datasource_getname below.
    test_student = Student(2)
    # We can see instance_pds but not _pds or module_pds
    # Yet it does't matter: because we can still mock its method by name
    name = test_student.name()
    assert name == "Sam"


@patch('employee.person_data_source.PersonDataSource.get_name_by_id')
def test_employee_name(mock_employee_datasource_getname):
    """
    The same test, except the target name of the mocked method
    """
    mock_employee_datasource_getname.return_value = "Bob"

    test_employee = employee.Employee(1)
    employee_name = test_employee.name()
    # NOTE: We switched the name "Bob" when Employee asked the DS for
    # it, but we didn't change what Employee did with it. In this case,
    # it applied formatting akin to a __repl__() so that's what we test
    # against.
    assert employee_name == "#1 - Bob"


def test_name__context_manager():
    """
    'patch' can be used in a context manager ('with...'). This style is
    good when you only want to patch a function during part of a test
    """

    # No patch here, works normally
    test_employee = employee.Employee(1)
    name = test_employee.name()
    assert name == "#1 - Alice"

    with patch('employee.person_data_source.PersonDataSource.get_name_by_id') as mock_employee_datasource_getname:
        # Set a side-effect for our mock object. If it is an iterable
        # each call will return the next value. It could call a function
        # defined here in the test.

        mock_employee_datasource_getname.side_effect = ['Bob', 'Tom']

        test_employee = employee.Employee(16)
        employee_name = test_employee.name()
        assert employee_name == "#16 - Bob"

        # Notice that it doesn't matter that we re-instantiate the
        # Student object, because we've patched the method - not the class.
        test_employee = employee.Employee(105)
        # This is the second time we are running the patched method
        employee_name = test_employee.name()
        assert employee_name == "#105 - Tom"


@patch('employee.person_data_source.PersonDataSource')
def test_name__class_patch(mock_datasource_class):
    """
    This example is for patching an entire CLASS. Most of the time you
    only need to patch a specific method!
    """

    # The return value from directly calling a class constructor is an
    # instance of the class. Because the patch above is for a whole
    # class, the return_value is a new mock object acting in place of
    # the instantiated object, just like any other call to the mock
    # object. On the mocked 'instance', the get_name_by_id method is
    # also a mock...
    mock_ds_instance = mock_datasource_class.return_value
    mock_instance_getname_function = mock_ds_instance.get_name_by_id
    mock_instance_getname_function.return_value = "Bob"

    # mock_datasource_class.return_value.get_name_by_id.return_value = "Bob"

    test_employee = employee.Employee(1)
    employee_name = test_employee.name()
    assert employee_name == "#1 - Bob"


def test_passing_in_mock_object():
    """
    Playing with an in-memory database as a test-double
    """
    humans = human_database.HumanDatabase()
    rows = humans.query("SELECT * FROM people where type = 'EMPLOYEE'")
    assert len(rows) == 4
    # No patch here, works normally
    with pytest.raises(human_database.sqlite3.DataError) as de_info:
        bad_employee = humans.get_name_by_id(120)

    employee_name = humans.get_name_by_id(4)
    assert employee_name == 'Darla'
    with patch('human_database.HumanDatabase.get_name_by_id') as mock_human_ds_getname:
        mock_human_ds_getname.return_value = 'Tammy'
        employee_name = humans.get_name_by_id(4)
        assert employee_name == 'Tammy'
