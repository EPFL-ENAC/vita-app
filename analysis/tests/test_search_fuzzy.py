from reader_scripts import search


def test_substitution():
    pattern = "abcde"
    string = "x abyde x"
    errors, regex_match = search.fuzzy_search(pattern, string, 1)

    assert regex_match is not None
    start_index, end_index = regex_match.span()

    assert errors == 1
    assert start_index == 2
    assert end_index == 7


def test_insertion():
    pattern = "abcde"
    string = "x abcyde x"
    errors, regex_match = search.fuzzy_search(pattern, string, 1)

    assert regex_match is not None
    start_index, end_index = regex_match.span()

    assert errors == 1
    assert start_index == 2
    assert end_index == 8


def test_deletion():
    pattern = "abcde"
    string = "x abde x"
    errors, regex_match = search.fuzzy_search(pattern, string, 1)

    assert regex_match is not None
    start_index, end_index = regex_match.span()

    assert errors == 1
    assert start_index == 2
    assert end_index == 6
