class PersonDataSource:
    """
    This is a simple representation of what could be
    a database or other source of data.
    """

    def __init__(self):
        self.names = {1: "Alice", 2: "Fred"}

    def get_name(self, person_id):
        return self.names.get(person_id, "UNKNOWN")
