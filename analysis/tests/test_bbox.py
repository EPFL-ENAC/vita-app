import sys
sys.path.insert(0, ".")

from BoundingBox import BoundingBox, Point


def createTestBbox():
    return BoundingBox(
        Point(0, 0),
        Point(2, 0),
        Point(0, 2),
        Point(2, 2)
    )


def testBarycenter():
    bbox = createTestBbox()
    center = Point(1, 1)
    computedCenter = bbox.getBarycenter()
    assert computedCenter.x == center.x
    assert computedCenter.y == center.y


def testContains():
    bbox = createTestBbox()
    assert bbox.contains(Point(1, 1))
    assert not bbox.contains(Point(-1, 1))
    assert not bbox.contains(Point(1, -1))
    assert not bbox.contains(Point(3, 1))
    assert not bbox.contains(Point(1, 3))
