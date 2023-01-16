class BoundingBox:
    """Bounding box with four points

    Args:
        bottomLeft (Point)
        bottomRight (Point)
        topLeft (Point)
        topRight (Point)
    """
    
    def __init__(self, bottomLeft, bottomRight, topLeft, topRight):
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.topLeft = topLeft
        self.topRight = topRight

    @property
    def points(self):
        """Return list of points ordered to draw the bounding box"""
        return [self.bottomLeft, self.bottomRight, self.topRight, self.topLeft]

    @staticmethod
    def fromData(data):
        """Creates new instance from dictionnary"""
        return BoundingBox(
            Point.fromData(data["bottomLeft"]),
            Point.fromData(data["bottomRight"]),
            Point.fromData(data["topLeft"]),
            Point.fromData(data["topRight"]),
        )


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toTuple(self):
        return (self.x, self.y)

    @staticmethod
    def fromData(data):
        """Creates new instance from dictionnary"""
        return Point(data["x"], data["y"])
