class DataSource:

    def __init__(self):
        self.names = {1: "Alice", 2: "Fred"}

    def get_name(self, id):
        return self.names.get(id, "UNKNOWN")
