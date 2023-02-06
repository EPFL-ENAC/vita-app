import json

from models.BoundingBox import BoundingBox


class DetectedText:
    """Container for text and bounding box

    Assumes that the bounding box's system of coordinates has its origin at
    the bottom left corner of the image/screen.

    Args:
        text (string)
        bbox (BoundingBox)
    """

    def __init__(self, text, bbox):
        self.text = text
        self.bbox = bbox

    @property
    def points(self):
        """Return list of points ordered to draw a bounding box"""
        return self.bbox.points

    @property
    def lineHeight(self):
        """Returns the bounding box height in 0 to 1 range"""
        return self.bbox.topLeft.y - self.bbox.bottomLeft.y

    @property
    def textWidth(self):
        """Returns the bounding box width in 0 to 1 range"""
        return self.bbox.bottomRight.x - self.bbox.bottomLeft.x

    def copy(self):
        return DetectedText(self.text, self.bbox.copy())

    @staticmethod
    def fromData(data):
        """Creates new instance from dictionnary"""
        return DetectedText(data["text"], BoundingBox.fromData(data["bbox"]))


def genListFromFile(filename):
    # Read JSON input
    f = open(filename)
    data = json.load(f)
    f.close()

    allDetectedText = []

    for d in data:
        allDetectedText.append(DetectedText.fromData(d))

    return allDetectedText
