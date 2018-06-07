from data_source import DataSource


class Person(object):
    def __init__(self):
        pass

    def name(self, person_id):
        ds = DataSource()
        return ds.get_name(person_id)
