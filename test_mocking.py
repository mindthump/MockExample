#!/usr/bin/env python

"""
The whole point of mocking is to monitor and/or alter the _behavior_
of running objects **without changing the original code**.

Let me say that python mocks are amazing. I like to use a metaphor
that a mock is a sci-fi robot spy with a cloaking device. (Or like the
super-realistic masks in 'Mission: Impossible'.) It's a chameleon that
will confidently answer any question asked of it. The answer can be a
programmed response or it can spawn other mocks.

There are three simple phases to a mock:

1. MAKE THE MOCK
A mock is usually created by
- instantiating the MagicMock() class directly
- patching, using a decorator or context manager

Patching is overriding existing code at execution time. Patch as small
as you can; whenever possible only the specific behavior that is
actually _used_, such as a single method's return value. However, if a
resource class is expensive or impossible to instantiate you may need to
patch the whole class (see test_class_patch below).

2. ARM THE MOCK
Configure the mock before deployment. Often the mock either has a
payload to deliver as a return_value on a callable, or some other
behavior as a side_effect().

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
utils.initialize_logging(console_log_level=logging.ERROR)
logging.info("Starting Tests...")


# ---------------- Basic method mocking
# NOTE: MAKE THE MOCK
@patch("people_data.PeopleDatabase.get_name_by_id")
def test_student(mock_student_getname_method):
    """
    Our patching target is the get_name_by_id() method on
    the PeopleDatabase class in the people_data module. The patch target
    is usually referred to by "<module>.<class>.<method>".

    @patch injects a new positional parameter to the decorated
    call signature, which we name 'mock_student_getname_method'
    in this case. The mock library pre-fills it with a MagicMock()
    object that will be substituted whenever the original
    PeopleDatabase.get_name_by_id() method _would_ have been
    called without the patch.
    """

    # Set the value which our mock object will return when the
    # get_name_by_id() function is called. "Sam" never appears in the data, so it
    # also acts as a guard from accidental false-positive tests.
    # NOTE: ARM THE MOCK
    mock_student_getname_method.return_value = "Sam"

    # TEST: Students should have "Hi!..." and name in badge text.
    # This looks just like a real call to the get_badge_text method
    # (e.g., in badges.py). We don't refer to the mock at all here; it's
    # already in place. The method's 'id' parameter is immaterial in this
    # case - since we override the call and fake the return value, the
    # input doesn't go anywhere.
    student_two = Student(2)
    # NOTE: FIRE IN THE HOLE
    student_two_badge_text = student_two.get_badge_text()
    logging.info("Student #2 name = '{}'".format(student_two_badge_text))

    # But the real Student #2 is Brenda -- we avoided the database fetch.
    assert student_two_badge_text == "HI! My name is Sam"


# ---------------- Pass mock object as argument
def test_volunteer():
    """
    It's a thing with a door and the world and a thing. (Never mind.)
    """
    people_datasource = people_data.PeopleDatabase("db://remote_person_ds/")
    people_datasource.connect()
    title = volunteer.Volunteer.get_badge_text(4, people_datasource)
    assert title == "** Intern **"

    # Instead of patching a real object with a mock object, we're
    # creating the mock ourselves and sending it "spelunking" into the
    # function as an argument. This is the technique most explanations
    # of mocking start with.
    # NOTE: MAKE THE MOCK
    mock_people_datasource = MagicMock()
    # Again, what the callable does with it is up to them, so equip your
    # mock accordingly. Give it a get_title_by_id method and give that
    # method a static return value.
    # NOTE: ARM THE MOCK
    mock_people_datasource.get_title_by_id.return_value = "Slave"

    # TEST: Volunteers just have their title on the badge
    # NOTE: FIRE IN THE HOLE
    title = volunteer.Volunteer.get_badge_text(4, mock_people_datasource)
    assert title == "** Slave **"
    # Demonstrate we actually called the mock once.
    assert mock_people_datasource.get_title_by_id.call_count == 1


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

    # Test that a call raises an expected exception; from py.test, not mocking!
    # IMHO this is a lot more readable than try/except.
    with pytest.raises(people_data.sqlite3.DataError):
        # There is no employee #16, this *will* raise an exception.
        employee.Employee(16).get_badge_text()

    # NOTE: MAKE THE MOCK
    with patch(
        "people_data.PeopleDatabase.get_name_by_id"
    ) as mock_employee_getname:
        # Set a side-effect for our mock object. If the 'side_effect' is
        # an iterable, each call will return the next value. It could
        # call a function, taking the original arguments. Neither of
        # these people are in the database.
        # TODO: Use itertools to make this inexhaustible?
        # NOTE: ARM THE MOCK
        mock_employee_getname.side_effect = ["Bob", "Tom"]

        # TEST: Employee badges should have Employee # and Name
        first_employee = employee.Employee(16)
        # NOTE: FIRE IN THE HOLE
        first_employee_badge_text = first_employee.get_badge_text()
        # Suddenly, there IS an employee #16 !!
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
# NOTE: MAKE THE MOCK
@patch("people_data.PeopleDatabase")
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

