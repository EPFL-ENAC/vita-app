from models.bounding_box import BoundingBox
from models.point import Point


def test_barycenter():
    bbox = BoundingBox.from_bounds(0, 2, 0, 2)
    center = Point(1, 1)
    computed_center = bbox.get_barycenter()
    assert computed_center.x == center.x
    assert computed_center.y == center.y


def testContains():
    bbox = BoundingBox.from_bounds(0, 2, 0, 2)
    assert bbox.contains_point(Point(1, 1))
    assert not bbox.contains_point(Point(-1, 1))
    assert not bbox.contains_point(Point(1, -1))
    assert not bbox.contains_point(Point(3, 1))
    assert not bbox.contains_point(Point(1, 3))
