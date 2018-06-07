import pytest
import pprint
from mock import patch
from person import Person


@patch('person.DataSource')
def test_name(mock_datasource):
    # This example is for patching an entire CLASS (DataSource)
    # Most of the time you only need to patch a specific method!!

    # Because the patch is for a class, the return_value is a mock instance
    # On the instance, the get_name() method is also a mock
    # So we can set the get_name method's return_value to "Bob"
    mock_datasource.return_value.get_name.return_value = "Bob"

    a_person = Person()
    name = a_person.name(person_id=1)
    assert name == "Bob"


def test_name_in_function():
    # This style is good when you only want to patch part of a function

    # No patch here, works normally
    a_person = Person()
    name = a_person.name(person_id=1)
    assert name == "Alice"

    with patch('person.DataSource') as mock_datasource:
        # set a return value for our mock object
        a_person = Person()
        mock_datasource.return_value.get_name.return_value = "Bob"
        name = a_person.name(person_id=1)
        assert name == "Bob"
