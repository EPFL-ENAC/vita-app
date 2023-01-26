import context
from readers import search


def testSubstitution():
    pattern = "abcde"
    string = "x abyde x"
    errors, regexMatch = search.fuzzySearch(pattern, string, 1)

    assert regexMatch is not None
    startIndex, endIndex = regexMatch.span()

    assert errors == 1
    assert startIndex == 2
    assert endIndex == 7


def testInsertion():
    pattern = "abcde"
    string = "x abcyde x"
    errors, regexMatch = search.fuzzySearch(pattern, string, 1)

    assert regexMatch is not None
    startIndex, endIndex = regexMatch.span()

    assert errors == 1
    assert startIndex == 2
    assert endIndex == 8


def testDeletion():
    pattern = "abcde"
    string = "x abde x"
    errors, regexMatch = search.fuzzySearch(pattern, string, 1)

    assert regexMatch is not None
    startIndex, endIndex = regexMatch.span()

    assert errors == 1
    assert startIndex == 2
    assert endIndex == 6
