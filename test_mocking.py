"""
Original Author: edc@mindthump.org
"""

import pytest
from unittest.mock import patch, MagicMock
import logging
from people.student import Student  # importing a specific class
from people import people_data, volunteer, employee, utils

# Example of overriding logger defaults.
utils.initialize_logging(console_log_level=logging.ERROR)
logging.info("Starting Tests...")


# ---------------- Decorate the function with a mock
@patch("people.people_data.PeopleDatabase.get_name_by_id")
@patch("people.people_data.PeopleDatabase.get_title_by_id")
def test_decorator(mock_student_get_title_method, mock_student_get_name_method):
    """
    NOTE: MAKE THE MOCK
    Here the mock is created though the function decorator. Our patching
    target is the `get_name_by_id()` and `get_title_by_id()` methods on the
    PeopleDatabase class in
    the people_data module. The patch target is usually referred to by
    "<module>.<class>.<method>".

    @patch injects new positional parameters to the decorated call
    signature, which we name 'mock_student_get_name_method' and
    'mock_student_get_title_method' in this case. (Note that when using
    more than one decorator, the added parameters appear in the reverse
    order of the decorators, from top to bottom.) The mock library
    automatically substitutes MagicMock() objects
    whenever the original methods _would_ have been called without the
    patch. However, only those two methods are overridden; calls to a
    different method would return the real results.

    Be aware that this technique mocks out the target method for any and
    all uses throughout the test function. If you need to mock only some
    calls, you will need to use a different technique.
    """

    # NOTE: ARM THE MOCK
    # Set the value which our mock object will return when the
    # get_name_by_id() function is called. "Sam" never appears in the
    # data, so it also acts as a guard against accidental false-positive
    # tests.
    mock_student_get_name_method.return_value = "Sam"
    mock_student_get_title_method.return_value = "Sophomore at UCLA"

    # TEST: Students should have "HI!..." with their name and title
    # in the badge text. This looks just like a real call to the
    # `get_badge_text()` method (e.g., in badges.py). We don't refer
    # to the mock at all here; it's already in place because of the
    # decorator. The method's 'id' parameter is immaterial in this case
    # - since we override the call and fake the return value, the input
    # doesn't go anywhere.
    student_two = Student(2)
    # NOTE: FIRE IN THE HOLE
    student_two_badge_text = student_two.get_badge_text()
    logging.info("Student #2 name = '{}'".format(student_two_badge_text))

    # But the real Student #2 is Brenda -- we avoided the database fetch.
    assert student_two_badge_text == "HI! My name is Sam (Sophomore at UCLA)"


# ---------------- Pass mock object as argument
def test_manual_mock():
    """
    It's a thing with a door and the world and a thing. (Never mind.)
    """
    # First, for contrast, is the 'real' value test using the DB. We
    # could not do this in the `test_decorator()` example above, because
    # the `get_badge_text()` method had already been mocked out by the
    # decorator for the entire function. We need the real database
    # for this. For volunteers, `get_badge_text()` is a class method.
    # It gets the badge text using a database reference passed as a
    # parameter.
    people_datasource = people_data.PeopleDatabase()
    title = volunteer.Volunteer.get_badge_text(4, people_datasource)
    assert title == "** Darla (Intern) **"

    # NOTE: MAKE THE MOCK
    # Instead of patching a particular method, we're creating the mock
    # ourselves and sending it "spelunking" into the function as an
    # argument. (Most explanations of mocking start with this is the
    # technique.) Begin by creating a mock of the whole database object.
    mock_people_datasource = MagicMock()

    # NOTE: ARM THE MOCK
    # What the called code does with it is up to them, so equip your
    # mock accordingly. Give it a `get_title_by_id()` method, which
    # itself is a MagicMock created just by using it. Give that method a
    # static return value. Do the same with `get_name_by_id()`.
    mock_people_datasource.get_title_by_id.return_value = "Satisfied User"
    mock_people_datasource.get_name_by_id.return_value = "Daisy"

    # NOTE: FIRE IN THE HOLE
    title = volunteer.Volunteer.get_badge_text(4, mock_people_datasource)
    assert title == "** Daisy (Satisfied User) **"
    # Demonstrate we actually called the mock exactly once using the
    # `call_count()` method.
    assert mock_people_datasource.get_title_by_id.call_count == 1


# ---------------- Patch as context manager
def test_context_manager():
    """
    'patch' can be used in a context manager ('with ...'). It works a
    lot like the first "test_decorator" example, but does not patch the
    entire function. Like the manual mocking example, this style is good
    when you want to patch a function during only part of a test.
    """

    # Not patched
    unpatched_employee = employee.Employee(1)
    unpatched_employee_badge = unpatched_employee.get_badge_text()
    assert unpatched_employee_badge == "#1 - Alice"

    # JUST FOR FUN
    # Test that a call raises an expected exception; from py.test, not mocking!
    # IMHO this is a lot more readable than try/except.
    with pytest.raises(people_data.sqlite3.DataError):
        # There is no employee #16, this *will* raise an exception.
        employee.Employee(16).get_badge_text()

    # TODO: Include employee titles. How to mock multiple values?
    # NOTE: MAKE THE MOCK
    with patch(
        "people.people_data.PeopleDatabase.get_name_by_id"
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
@patch("people.people_data.PeopleDatabase")
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
