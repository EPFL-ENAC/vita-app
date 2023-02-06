from models.BoundingBox import BoundingBox
from models.Point import Point


def testBarycenter():
    bbox = BoundingBox.fromBounds(0, 2, 0, 2)
    center = Point(1, 1)
    computedCenter = bbox.getBarycenter()
    assert computedCenter.x == center.x
    assert computedCenter.y == center.y


def testContains():
    bbox = BoundingBox.fromBounds(0, 2, 0, 2)
    assert bbox.containsPoint(Point(1, 1))
    assert not bbox.containsPoint(Point(-1, 1))
    assert not bbox.containsPoint(Point(1, -1))
    assert not bbox.containsPoint(Point(3, 1))
    assert not bbox.containsPoint(Point(1, 3))