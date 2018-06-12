from data_source import DataSource


class Person(object):
    def __init__(self, _id):
        self.id = _id

    def name(self):
        ds = DataSource()
        # This method call will be the target of our mocking.
        return ds.get_name(self.id)
