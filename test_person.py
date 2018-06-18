#!/usr/bin/env python

"""
The whole point of mocking is to monitor and/or alter the _behavior_
of running objects **without changing the original code**. Patch as
"small" as you can; whenever possible only the specific behavior that
is actually _used_. If a resource class is expensive or impossible to
instantiate you may need to patch the whole class.
"""

import pytest
# import pprint
from mock import patch, MagicMock
import employee  # the entire module
from student import Student  # a specific class
import volunteer
import people_data

_original_author = 'ed.cardinal@wdc.com'


@patch('student.PeopleDatabase.get_name_by_id')
def test_student(mock_student_getname):
    """
    A single method is the simplest to patch. The student.py module
    imports PersonDataSource directly so that's what we call it. The
    tricky part is knowing its name inside the running code; 'import'
    statements are a good clue.
    """

    # Set the value our mock object will return for the mocked
    # get_name_by_id() function. The id argument is immaterial in this
    # case - since we override the return value, the input doesn't go
    # anywhere. "Sam" never appears in the data, so it also acts as a
    # guard from accidental false-positive tests.
    mock_student_getname.return_value = "Sam"

    name = Student(2).get_name()
    assert name == "Sam"


@patch('employee.people_data.PeopleDatabase.get_name_by_id')
def test_employee(mock_employee_getname):
    """
    The same test, except the target name of the mocked method
    """
    mock_employee_getname.return_value = "Bob"
    employee_name = employee.Employee(1).get_name()

    # NOTE: Why don't we assert == "Bob"?
    # We switched the name to "Bob" when Employee asked the database
    # for it, but we didn't change what Employee did with it after
    # we switched it. In this case, it applied formatting akin to a
    # __repl__() then returned that, so that's what we test against.
    assert employee_name == "#1 - Bob"


def test_volunteer():
    """
    It's a thing with the door and the world and a thing. (Never mind).
    """
    _pds = people_data.PeopleDatabase("db://remote_person_ds/")
    title = volunteer.Volunteer.get_title(4, _pds)
    assert title == "** Intern **"

    # We're sending the mock object "spelunking" into the function as an argument.
    # This is the technique most explanations of mocking start with.
    mock_database = MagicMock()
    # Again, what the callable does with it is up to them, so equip your mock accordingly.
    # Give it a get_title_by_id method and give that method a static return value.
    mock_database.get_title_by_id.return_value = "Slave"
    title = volunteer.Volunteer.get_title(4, mock_database)
    assert title == "** Slave **"


def test_context_manager():
    """
    'patch' can be used in a context manager ('with...'). This style is
    good when you only want to patch a function during part of a test
    """

    # No patch here, works normally
    name = employee.Employee(1).get_name()
    assert name == "#1 - Alice"

    with patch('employee.people_data.PeopleDatabase.get_name_by_id') as mock_employee_getname:
        # Set a side-effect for our mock object. If it is an iterable
        # each call will return the next value. It could call a function,
        # taking the original arguments.

        mock_employee_getname.side_effect = ['Bob', 'Tom']

        _employee = employee.Employee(16)
        employee_name = _employee.get_name()
        assert employee_name == "#16 - Bob"

        # Notice that it doesn't matter that we re-instantiate the
        # Student object, because we've patched the method - not the class.
        _employee = employee.Employee(105)
        # This is the second time we are running the patched method
        employee_name = _employee.get_name()
        assert employee_name == "#105 - Tom"

        # We could also look at argument values on the calls, values set
        # on the mock by the method, and much more
        assert mock_employee_getname.call_count == 2


@patch('employee.people_data.PeopleDatabase')
def test_class_patch(mock_datasource_class):
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
    employee_name = test_employee.get_name()
    assert employee_name == "#1 - Bob"


def test_misc_concepts():
    """
    """
    # TODO: mock_open

    # Directly accessing things I shouldn't (_query)
    humans = people_data.PeopleDatabase("db://remote_person_ds/")
    rows = humans._query("SELECT * FROM people where type = 'EMPLOYEE'")
    assert len(rows) == 4

    # Expected Exception: this is a lot more readable than try/except
    with pytest.raises(people_data.sqlite3.DataError):
        humans.get_name_by_id(120)
