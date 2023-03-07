import regex
from models.bounding_box import BoundingBox
from models.detected_text import DetectedText
from reader_scripts import search

pattern1 = "abcde"
pattern2 = "fghij"

reference = DetectedText(pattern1, BoundingBox.from_bounds(0, 1, 1, 2))
top_right = DetectedText(pattern2, BoundingBox.from_bounds(1, 2, 2, 3))
right = DetectedText(pattern2, BoundingBox.from_bounds(1, 2, 1, 2))
bottom_right = DetectedText(pattern2, BoundingBox.from_bounds(1, 2, 0, 1))
below = DetectedText(pattern2, BoundingBox.from_bounds(0, 1, 0, 1))

detected_text_list = [reference, top_right, right, bottom_right, below]

dummy_match = regex.match("", "")
reference = search.Candidate(reference, 0, dummy_match)


def test_string_on_same():
    candidate = search.search_string_on_right(
        reference, detected_text_list, pattern1, 1
    )
    assert len(candidate) != 0
    assert candidate[0].detected_text.text == reference.detected_text.text
    # detected_text themselves are different because candidate.detexted_text is
    # rewritten in search.string_on_right


def test_string_on_right():
    candidate = search.search_string_on_right(
        reference, detected_text_list, pattern2, 1
    )
    assert len(candidate) != 0
    assert candidate[0].detected_text is right


def test_string_below():
    candidate = search.search_string_below(
        reference, detected_text_list, pattern2
    )
    assert len(candidate) != 0
    assert candidate[0].detected_text is below
