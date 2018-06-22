#!/usr/bin/env python

"""
The whole point of mocking is to monitor and/or alter the _behavior_
of running objects **without changing the original code**. Patch as
"small" as you can; whenever possible only the specific behavior that
is actually _used_. If a resource class is expensive or impossible to
instantiate you may need to patch the whole class (see test_class_patch
below).
"""

import pytest
from mock import patch, MagicMock
import logging
import utils
import employee  # the entire module
from student import Student  # a specific class
import volunteer
import people_data

# Example of overriding logger defaults.
utils.initialize_logging(console_log_level=logging.INFO)
logging.info("Starting Tests...")

_original_author = 'ed.cardinal@wdc.com'


# Target imports class
@patch('student.PeopleDatabase.get_name_by_id')
def test_student(mock_student_getname):
    """
    A single method is the simplest to patch. The student.py module
    imports PersonDataSource directly so that's what we call it. The
    tricky part is knowing its name inside the running code; 'import'
    statements are a good clue.

    Also note that we don't import the student module into this module,
    only the Student class. So why can we mock "student.PeopleDatabase"
    above? Because it's just a string until the mock package is ready to
    use it in place, and at that time it will be in scope.

    Set the value which our mock object will return when the
    get_name_by_id() function is called. The id argument is immaterial
    in this case - since we override the return value, the input doesn't
    go anywhere. "Sam" never appears in the data, so it also acts as a
    guard from accidental false-positive tests.
    """
    mock_student_getname.return_value = "Sam"

    # This looks just like a real call to the get_name method
    student_two = Student(2)
    student_two_name = student_two.get_name()
    logging.info("Student #2 name = '{}'".format(student_two_name))

    # But the real Student #2 is Brenda, we avoided the database fetch
    assert student_two_name == "Sam"


# Target imports module
@patch('employee.people_data.PeopleDatabase.get_name_by_id')
def test_employee(mock_employee_getname):
    """
    The same test, except the target name of the mocked method
    """
    mock_employee_getname.return_value = "Bob"
    employee_name = employee.Employee(1).get_name()
    logging.warning("Employee #1 = '{}'".format(employee_name))

    assert employee_name == "#1 - Bob"  # NOTE: Why don't we assert == "Bob"?  # We
    # switched the name to "Bob" when Employee asked the database  # for it,
    # but we didn't change what Employee did with it after we  # switched it. In this
    # case, it applied formatting, so that's what  # we test against.


# Pass mock object as argument
def test_volunteer():
    """
    It's a thing with the door and the world and a thing. (Never mind).
    """
    _pds = people_data.PeopleDatabase("db://remote_person_ds/")
    title = volunteer.Volunteer.get_title(4, _pds)
    assert title == "** Intern **"

    # Instead of patching a real object with a mock object, we're
    # creating the mock ourselves and sending it "spelunking" into the
    # function as an argument. This is the technique most explanations
    # of mocking start with.
    mock_database = MagicMock()
    # Again, what the callable does with it is up to them, so equip your
    # mock accordingly. Give it a get_title_by_id method and give that
    # method a static return value.
    mock_database.get_title_by_id.return_value = "Slave"
    title = volunteer.Volunteer.get_title(4, mock_database)
    assert title == "** Slave **"


# Patch as context manager
def test_context_manager():
    """
    'patch' can be used in a context manager ('with ...'). This style is
    good when you want to patch a function during only part of a test
    """

    # Not patched
    unpatched_employee = employee.Employee(1).get_name()
    assert unpatched_employee == "#1 - Alice"

    with patch('employee.people_data.PeopleDatabase.get_name_by_id') as mock_employee_getname:
        # Set a side-effect for our mock object. If it is an iterable
        # each call will return the next value. It could call a function,
        # taking the original arguments.
        mock_employee_getname.side_effect = ['Bob', 'Tom']

        patched_employee = employee.Employee(16)
        employee_name = patched_employee.get_name()
        assert employee_name == "#16 - Bob"

        # Notice that it doesn't matter that we re-instantiate the
        # Student object, because we've patched the method - not the class.
        second_patched_employee = employee.Employee(105)
        # This is the second time we are running the patched method
        employee_name = second_patched_employee.get_name()
        assert employee_name == "#105 - Tom"

        # We can look at if it was called, how many times, argument
        # values on the calls, values set on the mock by the method, and
        # much more
        assert mock_employee_getname.call_count == 2


# Patch entire class
@patch('employee.people_data.PeopleDatabase')
def test_class_patch(mock_datasource_class):
    """
    Occasionally you need to patch an entire CLASS. One reason might
    be that instantiating the class at all is expensive or impossible
    (e.g., a firewalled resource). The return value from calling a
    normal class constructor is an _instance_ of the class. Because
    the patch above is for the whole class, the return_value is a new
    mock object acting in place of the instantiated object, just like
    any other call to the mock object. On the mocked 'instance', the
    get_name_by_id method is also a mock...
    """
    mock_datasource_class.return_value.get_name_by_id.return_value = "Bob"
    employee_name = employee.Employee(1).get_name()
    assert employee_name == "#1 - Bob"


# Test call raises exception
def test_raises_exception():
    """
    Expected Exception: IMHO this is a lot more readable than try/except
    From py.test, not mocking!
    """

    humans = people_data.PeopleDatabase("db://remote_person_ds/")
    with pytest.raises(people_data.sqlite3.DataError):
        humans.get_name_by_id(120)


# Running from commandline w/o py.test
def main():
    test_student()
    test_employee()
    test_volunteer()
    test_raises_exception()
    test_class_patch()
    test_context_manager()


if __name__ == "__main__":
    main()
