import sys
sys.path.insert(0, ".")

from readers import search
from DetectedText import DetectedText
from BoundingBox import BoundingBox, Point


pattern1 = "abcde"
pattern2 = "fghij"

reference = DetectedText(
    pattern1,
    BoundingBox(Point(0, 1), Point(1, 1), Point(0, 2), Point(1, 2))
)

topRight = DetectedText(
    pattern2,
    BoundingBox(Point(1, 2), Point(2, 2), Point(1, 3), Point(2, 3))
)

right = DetectedText(
    pattern2,
    BoundingBox(Point(1, 1), Point(2, 1), Point(1, 2), Point(2, 2))
)

bottomRight = DetectedText(
    pattern2,
    BoundingBox(Point(1, 0), Point(2, 0), Point(1, 1), Point(2, 1))
)

below = DetectedText(
    pattern2,
    BoundingBox(Point(0, 0), Point(1, 0), Point(0, 1), Point(1, 1))
)

detectedTextList = [reference, topRight, right, bottomRight, below]


def testStringOnSame():
    candidate = search.stringOnRight(reference, detectedTextList, pattern1, 1)
    assert candidate is not None
    assert candidate.detectedText is reference


def testStringOnRight():
    candidate = search.stringOnRight(reference, detectedTextList, pattern2, 1)
    assert candidate is not None
    assert candidate.detectedText is right


def testStringBelow():
    candidate = search.stringBelow(reference, detectedTextList, pattern2)
    assert candidate is not None
    assert candidate.detectedText is below
