import sys
sys.path.insert(0, ".")

from BoundingBox import BoundingBox, Point


def testBarycenter():
    bbox = BoundingBox.fromBounds(0, 2, 0, 2)
    center = Point(1, 1)
    computedCenter = bbox.getBarycenter()
    assert computedCenter.x == center.x
    assert computedCenter.y == center.y


def testContains():
    bbox = BoundingBox.fromBounds(0, 2, 0, 2)
    assert bbox.contains(Point(1, 1))
    assert not bbox.contains(Point(-1, 1))
    assert not bbox.contains(Point(1, -1))
    assert not bbox.contains(Point(3, 1))
    assert not bbox.contains(Point(1, 3))
