#!/usr/bin/env python

import pytest
import pprint
from mock import patch
import employee  # the entire module
from student import Student  # a specific class

"""
The whole point of mocking is to monitor and/or alter the __behavior__ of running
objects **without changing the original code**.
Patch as "small" as you can; whenever possible only the specific behavior that is 
actually __used__.
Exception: if a resource class is expensive or impossible to instantiate you may need 
to patch the whole class.
"""


@patch('student.PersonDataSource.get_name')
def test_student_name(mock_student_datasource_getname):
    """
    A single method is the simplest to patch.
    The student.py module imports PersonDataSource directly so that's what we call it.
    The tricky part is knowing
    its name inside the running code; 'import' statements are a good
    clue.
    """

    # Set the value our mock object will return for the mocked get_name() function
    mock_student_datasource_getname.return_value = "Sam"
    test_student = Student(2)
    # We can see instance_pds but not _pds or module_pds
    # Yet it does't matter: because we can still mock its method by name
    name = test_student.name()
    assert name == "Sam"


@patch('employee.person_data_source.PersonDataSource.get_name')
def test_employee_name(mock_employee_datasource_getname):
    """
    The same test, except the target name of the mocked method
    """
    mock_employee_datasource_getname.return_value = "Bob"

    test_employee = employee.Employee(1)
    employee_name = test_employee.name()
    assert employee_name == "Bob"


def test_name__context_manager():
    """
    'patch' can be used in a context manager ('with...').
    This style is good when you only want to patch a function during part of a test
    """

    # No patch here, works normally
    test_employee = employee.Employee(1)
    name = test_employee.name()
    assert name == "Alice"


    with patch('employee.person_data_source.PersonDataSource.get_name') as mock_employee_datasource_getname:
            # Set a side-effect for our mock object. If it is an iterable
            # each call will return the next value. It could call a function
            # defined here in the test.

            mock_employee_datasource_getname.side_effect = ['Bob', 'Tom']

            test_employee = employee.Employee(105)
            employee_name = test_employee.name()
            assert employee_name == "Bob"

            # Notice that it doesn't matter that we re-instantiate the
            # Student object, because we've patched the method - not the class.
            test_employee = employee.Employee(105)
            # This is the second time we are running the patched method
            employee_name = test_employee.name()
            assert employee_name == "Tom"


@patch('employee.person_data_source.PersonDataSource')
def test_name__class_patch(mock_datasource_class):
    """
    This example is for patching an entire CLASS.
    Most of the time you only need to patch a specific method!
    """

    # The return value from directly calling a class is an instance of the class.
    # Because the patch above is for a whole class, the return_value is a new
    # mock object acting in place of the instantiated object. On the
    # mocked 'instance', the get_name method is also a mock...
    mock_ds_instance = mock_datasource_class.return_value
    mock_instance_getname_function = mock_ds_instance.get_name
    mock_instance_getname_function.return_value = "Bob"

    # mock_datasource_class.return_value.get_name.return_value = "Bob"

    test_employee = employee.Employee(1)
    employee_name = test_employee.name()
    assert employee_name == "Bob"
