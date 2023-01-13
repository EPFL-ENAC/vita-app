import sys

sys.path.insert(0, ".")

from readers import search


def testSubstitution():
    pattern = "abcde"
    string = "x abyde x"
    errors, startIndex, endIndex = search.fuzzySearch(pattern, string, 1)
    assert errors == 1
    assert startIndex == 2
    assert endIndex == 7


def testInsertion():
    pattern = "abcde"
    string = "x abcyde x"
    errors, startIndex, endIndex = search.fuzzySearch(pattern, string, 1)
    assert errors == 1
    assert startIndex == 2
    assert endIndex == 8


def testDeletion():
    pattern = "abcde"
    string = "x abde x"
    errors, startIndex, endIndex = search.fuzzySearch(pattern, string, 1)
    assert errors == 1
    assert startIndex == 2
    assert endIndex == 6
