class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toTuple(self):
        return (self.x, self.y)

    def copy(self):
        return Point(self.x, self.y)

    @staticmethod
    def from_data(data):
        """Creates new instance from dictionnary"""
        return Point(data["x"], data["y"])
