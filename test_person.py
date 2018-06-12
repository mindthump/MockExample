import pytest
import pprint
from mock import patch
import person

"""
The whole point of mocking is to monitor and/or alter the behavior of running
objects without changing the original code.
"""


# A single method is the simplest to patch. The tricky part is knowing
# its name inside the running code; 'import' statements are a good clue.
# Here, 'person' is the module under test, 'DataSource' is a class inside
# the 'person' module, and 'get_name' is a method of the 'DataSource' class.
@patch('person.DataSource.get_name')
def test_name__method_patch(mock_datasource_getname):
    # Set the value our mock object will return for the mocked get_name() function
    mock_datasource_getname.return_value = "Bob"

    a_person = person.Person()
    name = a_person.name(person_id=1)
    assert name == "Bob"


def test_name_inside_function():
    """
    'patch' can be used in a context manager ('with...').
    This style is good when you only want to patch a function during part of a test
    """

    # No patch here, works normally
    a_person = person.Person()
    name = a_person.name(person_id=1)
    assert name == "Alice"

    with patch('person.DataSource.get_name') as mock_datasource_getname:
        # set a return value for our mock object
        a_person = person.Person()
        mock_datasource_getname.return_value = "Bob"
        name = a_person.name(person_id=1)
        assert name == "Bob"


@patch('person.DataSource')
def test_name__class_patch(mock_datasource_class):
    # This example is for patching an entire CLASS.
    # Most of the time you only need to patch a specific method!

    # Because the patch is for a whole class, the return_value is a new
    # mock object acting in place of the instantiated object. On the
    # mocked 'instance', the get_name method is also a mock...
    mock_datasource_instance = mock_datasource_class.return_value

    # ... so we can set the get_name() mock method's return_value to Bob
    mock_datasource_instance.get_name.return_value = "Bob"

    # All at once:
    # mock_datasource_class.return_value.get_name.return_value = "Bob"

    a_person = person.Person()
    name = a_person.name(person_id=1)
    assert name == "Bob"
