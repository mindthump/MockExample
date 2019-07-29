#!/usr/bin/env python

"""
The whole point of mocking is to monitor and/or alter the _behavior_
of running objects **without changing the original code**.

Let me say that python mocks are amazing. I like to use a metaphor that
a mock is a sci-fi robot spy with a cloaking device. It's a chameleon
that will confidently answer any question asked of it. The answer can be
a programmed response or it can spawn another mock. It generally just
works by itself.

There are three simple phases to a mock:

1. MAKE THE MOCK
A mock is usually created by
- instantiating the MagicMock() class directly
- patching, using a decorator or context manager

Patching is overriding existing code at execution time. Patch as small
as you can; whenever possible only the specific behavior that is
actually _used_, such as a single method's return value. If a resource
class is expensive or impossible to instantiate you may need to patch
the whole class (see test_class_patch below).

2. ARM THE MOCK
Often the mock either has a payload to deliver as a return_value on a callable,
or some other behavior as a side_effect().

3. FIRE IN THE HOLE
You trigger the behavior exactly like you would if you were using the
real resource: the code under test doesn't change at all. How cool is
that?

Original Author: edc@mindthump.org
"""

import pytest
from unittest.mock import patch, MagicMock
import logging
import utils
import employee  # importing the entire module
from student import Student  # importing a specific class
import volunteer
import people_data

# Example of overriding logger defaults.
utils.initialize_logging()
logging.info("Starting Tests...")


# ---------------- Target imports class
# NOTE: MAKE THE MOCK
@patch("student.PeopleDatabase.get_name_by_id")
def test_student(mock_student_getname_method):
    """
    A single method is the simplest to patch.

    Our patching target is the get_name_by_id() method on the PeopleDatabase class.

    Over in the student.py module, we use this form of import:
    >> from people_data import PeopleDatabase
    Purposely avoiding all discussions of namespaces, the student
    module pulls the PersonDataSource class definition directly "into"
    itself. We can now reference it as student.PeopleDatabase, and the
    target method as "student.PeopleDatabase.get_name_by_id" in the
    @patch() decorator.

    Also note that we don't import the student module into this test module,
    only the Student class. So why can we mock "student.PeopleDatabase"
    above? Because it's just a string until the mock package is ready to
    use it in place, and at that time it will be in scope.
    """

    # Set the value which our mock object will return when the
    # get_name_by_id() function is called. The id argument is immaterial
    # in this case - since we override the return value, the input doesn't
    # go anywhere. "Sam" never appears in the data, so it also acts as a
    # guard from accidental false-positive tests.
    # NOTE: ARM THE MOCK
    mock_student_getname_method.return_value = "Sam"

    # This looks just like a real call to the get_badge_text method, e.g. in badges.py
    # We don't refer to the mock at all here, it's already in place.
    # NOTE: FIRE IN THE HOLE
    student_two = Student(2)
    student_two_name = student_two.get_badge_text()
    logging.info("Student #2 name = '{}'".format(student_two_name))

    # But the real Student #2 is Brenda, we avoided the database fetch
    assert student_two_name == "HI! My name is Sam"


# ---------------- Target imports module
# NOTE: MAKE THE MOCK
@patch("employee.people_data.PeopleDatabase.get_name_by_id")
def test_employee(mock_employee_getname):
    """
    Q: What exactly are we patching here?
    'employee' = module imported into _this_ module, above
    'people_data' = module imported into 'employee' module
    'PeopleDatabase' = class defined in 'people_data' module
    'get_name_by_id' = method defined in 'PeopleDatabase' class

    A: We're only patching a single *method*, get_name_by_id(). But look
    at the circuitous route we take to get there! Why? Because we need to
    follow the trail of imports and definitions down to the precise place
    the target function is _used_. When the function is about to be called,
    the function is short-circuited to the mock, enabling us to alter return
    values and track method usage.
    """
    # NOTE: ARM THE MOCK
    mock_employee_getname.return_value = "Bob"
    # NOTE: FIRE IN THE HOLE
    employee_badge_text = employee.Employee(1).get_badge_text()
    logging.warning("Employee #1 = '{}'".format(employee_badge_text))

    assert employee_badge_text == "#1 - Bob"
    # NOTE: Why don't we assert == "Bob"?
    # We switched the name to Bob when Employee asked the database
    # for it, but we didn't change what Employee did with it after we
    # switched it. In this case it applied formatting, so that's what
    # we test against.


# ---------------- Pass mock object as argument
def test_volunteer():
    """
    It's a thing with a door and the world and a thing. (Never mind.)
    """
    _pds = people_data.PeopleDatabase("db://remote_person_ds/")
    _pds.connect()
    title = volunteer.Volunteer.get_badge_text(4, _pds)
    assert title == "** Intern **"

    # Instead of patching a real object with a mock object, we're
    # creating the mock ourselves and sending it "spelunking" into the
    # function as an argument. This is the technique most explanations
    # of mocking start with.
    # NOTE: MAKE THE MOCK
    mock_database = MagicMock()
    # Again, what the callable does with it is up to them, so equip your
    # mock accordingly. Give it a get_title_by_id method and give that
    # method a static return value.
    # NOTE: ARM THE MOCK
    mock_database.get_title_by_id.return_value = "Slave"
    # NOTE: FIRE IN THE HOLE
    title = volunteer.Volunteer.get_badge_text(4, mock_database)
    assert title == "** Slave **"


# ---------------- Patch as context manager
def test_context_manager():
    """
    'patch' can be used in a context manager ('with ...'). This style is
    good when you want to patch a function during only part of a test.

    """

    # Not patched
    unpatched_employee = employee.Employee(1)
    unpatched_employee_badge = unpatched_employee.get_badge_text()
    assert unpatched_employee_badge == "#1 - Alice"

    # NOTE: MAKE THE MOCK
    with patch(
        "employee.people_data.PeopleDatabase.get_name_by_id"
    ) as mock_employee_getname:
        # 'mock_employee_getname' is now a MagicMock()
        # which will be substituted whenever the original
        # employee.people_data.PeopleDatabase.get_name_by_id method
        # _would_ have been called without the patch. No individual
        # employee's get_name_by_id method is patched, the patch is on
        # the method in the class.

        # Set a side-effect for our mock object. If the 'side_effect' is
        # an iterable, each call will return the next value. It could
        # call a function, taking the original arguments. Neither of
        # these people are in the database.
        # TODO: Use itertools to make this inexhaustible?
        # NOTE: ARM THE MOCK
        mock_employee_getname.side_effect = ["Bob", "Tom"]

        # NOTE: FIRE IN THE HOLE
        first_employee = employee.Employee(16)
        first_employee_badge_text = first_employee.get_badge_text()
        assert first_employee_badge_text == "#16 - Bob"

        # Notice that it doesn't matter that we re-instantiate the
        # object, because we've patched the method - not the class.
        second_employee = employee.Employee(105)
        # This is the second time we are running the patched method
        second_employee_badge_text = second_employee.get_badge_text()
        assert second_employee_badge_text == "#105 - Tom"

        # We can look at if it was called, how many times, argument
        # values on the calls, values set on the mock by the method, and
        # much more
        assert mock_employee_getname.call_count == 2


# ---------------- Patch entire class
@patch("employee.people_data.PeopleDatabase")
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
    # NOTE: ARM THE MOCK
    mock_datasource_instance = mock_datasource_class.return_value
    mock_getnamebyid_method = mock_datasource_instance.get_name_by_id
    mock_getnamebyid_method.return_value = "Bob"
    # NOTE: FIRE IN THE HOLE
    employee_name = employee.Employee(1).get_badge_text()
    assert employee_name == "#1 - Bob"


# Test that a call raises an expected exception; from py.test, not mocking!
def test_raises_exception():
    """
    IMHO this is a lot more readable than try/except
    """

    humans = people_data.PeopleDatabase("db://remote_person_ds/")
    humans.connect()
    with pytest.raises(people_data.sqlite3.DataError):
        humans.get_name_by_id(120)
