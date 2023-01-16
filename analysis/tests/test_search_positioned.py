import sys
sys.path.insert(0, ".")

from readers import search
from DetectedText import DetectedText
from BoundingBox import BoundingBox, Point


pattern1 = "abcde"
pattern2 = "fghij"

reference   = DetectedText(pattern1, BoundingBox.fromBounds(0, 1, 1, 2))
topRight    = DetectedText(pattern2, BoundingBox.fromBounds(1, 2, 2, 3))
right       = DetectedText(pattern2, BoundingBox.fromBounds(1, 2, 1, 2))
bottomRight = DetectedText(pattern2, BoundingBox.fromBounds(1, 2, 0, 1))
below       = DetectedText(pattern2, BoundingBox.fromBounds(0, 1, 0, 1))

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
