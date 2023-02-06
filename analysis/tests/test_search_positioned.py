import regex
from models.BoundingBox import BoundingBox
from models.DetectedText import DetectedText
from readerScripts import search

pattern1 = "abcde"
pattern2 = "fghij"

reference = DetectedText(pattern1, BoundingBox.fromBounds(0, 1, 1, 2))
topRight = DetectedText(pattern2, BoundingBox.fromBounds(1, 2, 2, 3))
right = DetectedText(pattern2, BoundingBox.fromBounds(1, 2, 1, 2))
bottomRight = DetectedText(pattern2, BoundingBox.fromBounds(1, 2, 0, 1))
below = DetectedText(pattern2, BoundingBox.fromBounds(0, 1, 0, 1))

detectedTextList = [reference, topRight, right, bottomRight, below]

dummyMatch = regex.match("", "")
reference = search.Candidate(reference, 0, dummyMatch)


def testStringOnSame():
    candidate = search.stringOnRight(reference, detectedTextList, pattern1, 1)
    assert len(candidate) != 0
    assert candidate[0].detectedText.text == reference.detectedText.text
    # detectedText themselves are different because candidate.detextedText is
    # rewritten in search.stringOnRight


def testStringOnRight():
    candidate = search.stringOnRight(reference, detectedTextList, pattern2, 1)
    assert len(candidate) != 0
    assert candidate[0].detectedText is right


def testStringBelow():
    candidate = search.stringBelow(reference, detectedTextList, pattern2)
    assert len(candidate) != 0
    assert candidate[0].detectedText is below
