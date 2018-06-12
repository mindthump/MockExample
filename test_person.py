import pytest
import pprint
from mock import patch
import person

"""
The whole point of mocking is to monitor and/or alter the behavior of running
objects without changing the original code.
"""


@patch('person.PersonDataSource.get_name')
def test_name__method_patch(mock_datasource_getname):
    """
    A single method is the simplest to patch. The tricky part is knowing
    its name inside the running code; 'import' statements are a good
    clue. Here, 'person' is the module under test, 'PersonDataSource' is a
    class inside the 'person' module, and 'get_name' is a method of the
    'PersonDataSource' class.
    """

    # Set the value our mock object will return for the mocked get_name() function
    mock_datasource_getname.return_value = "Bob"

    a_person = person.Person(1)
    name = a_person.name()
    assert name == "Bob"


def test_name_inside_function():
    """
    'patch' can be used in a context manager ('with...').
    This style is good when you only want to patch a function during part of a test
    """

    # No patch here, works normally
    a_person = person.Person(1)
    name = a_person.name()
    assert name == "Alice"

    with patch('person.PersonDataSource.get_name') as mock_datasource_getname:
        # Set a side-effect for our mock object. If it is an iterable
        # each call will return the next value. It could call a function
        # defined here in the test.
        mock_datasource_getname.side_effect = ['Bob', 'Tom']

        name = a_person.name()
        assert name == "Bob"

        # Notice that it doesn't matter that we re-instantiate the
        # Person object, because we've patched the method - not the class.
        a_person = person.Person(105)
        name = a_person.name()
        assert name == "Tom"


@patch('person.PersonDataSource')
def test_name__class_patch(mock_datasource_class):
    """
    This example is for patching an entire CLASS.
    Most of the time you only need to patch a specific method!
    """

    # Because the patch is for a whole class, the return_value is a new
    # mock object acting in place of the instantiated object. On the
    # mocked 'instance', the get_name method is also a mock...
    mock_datasource_instance = mock_datasource_class.return_value

    # ... so we can set the get_name() mock method's return_value
    mock_datasource_instance.get_name.return_value = "Bob"

    # All at once:
    # mock_datasource_class.return_value.get_name.return_value = "Bob"

    a_person = person.Person(1)
    name = a_person.name()
    assert name == "Bob"
