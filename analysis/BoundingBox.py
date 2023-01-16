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

    def getBarycenter(self):
        center = Point(0., 0.)

        for p in self.points:
            center.x += p.x
            center.y += p.y

        center.x /= 4
        center.y /= 4

        return center

    def contains(self, point):
        """Check if point is inside the bounding box

        Note: Assumes that boxes are rectangular and not rotated, to simplify
        computation.
        """
        if point.x < self.bottomLeft.x: return False
        if point.y < self.bottomLeft.y: return False
        if point.x > self.topRight.x: return False
        if point.y > self.topRight.y: return False
        return True


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
