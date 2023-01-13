import json


class DetectedText:
    """Container for text and bounding box

    Args:
        text (string)
        bottomLeft (Point)
        bottomRight (Point)
        topLeft (Point)
        topRight (Point)
    """

    def __init__(self, text, bottomLeft, bottomRight, topLeft, topRight):
        self.text = text
        self.bottomLeft = bottomLeft
        self.bottomRight = bottomRight
        self.topLeft = topLeft
        self.topRight = topRight

    @property
    def points(self):
        """Return list of points ordered to draw a bounding box"""
        return [self.bottomLeft, self.bottomRight, self.topRight, self.topLeft]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def toTuple(self):
        return (self.x, self.y)


def pointFromData(data):
    return Point(data["x"], data["y"])


def fromFile(filename):
    # Read JSON input
    f = open(filename)
    data = json.load(f)
    f.close()

    allDetectedText = []

    for d in data:
        bbox = d["bbox"]
        allDetectedText.append(
            DetectedText(
                d["text"],
                pointFromData(bbox["bottomLeft"]),
                pointFromData(bbox["bottomRight"]),
                pointFromData(bbox["topLeft"]),
                pointFromData(bbox["topRight"]),
            )
        )

    return allDetectedText
