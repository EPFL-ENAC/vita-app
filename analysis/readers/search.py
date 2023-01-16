import regex
import config


def fuzzySearch(pattern, string, errorMax):
    """Find approximately matching pattern in string

    Args:
        pattern (string): regex pattern
        string (string): where search is performed
        errorMax (int)

    Returns:
        errors (int | None): None if no match
        startIndex (int)
        endIndex (int): excluded
    """
    regexPattern = f"({pattern}){{e<={errorMax}}}"
    match = regex.search(regexPattern, string, regex.BESTMATCH)

    if match is None:
        return None, 0, 0

    # match.fuzzy_counts: (n_substitutions, n_insertions, n_deletes)
    errors = sum(match.fuzzy_counts)
    startIndex, endIndex = match.span()

    return errors, startIndex, endIndex


class Candidate:
    """Container for DetectedText instance and fuzzySearch reasult"""

    def __init__(self, detectedText, errors, startIndex, endIndex):
        self.detectedText = detectedText
        self.errors = errors
        self.startIndex = startIndex
        self.endIndex = endIndex


def string(detectedTextList, pattern, nCandidates=1, region=None):
    """Searches for a string in all provided detected texts

    Args
        detectedTextList ([detectedText])
        pattert (string): regex pattern
        nCandidates (int): number of candidates to return
        region (BoundingBox | None): check if candidate bounding box's center
            is inside region

    Returns:
        candidates ([Candidates]): nCandidates first candidates matching the
            pattern
    """

    candidates = []

    for detectedText in detectedTextList:
        if region is not None:
            center = detectedText.bbox.getBarycenter()
            if not region.contains(center): continue

        error, startIndex, endIndex = fuzzySearch(
            pattern, detectedText.text, config.ERROR_MAX
        )

        if error is None:
            continue
        candidates.append(Candidate(detectedText, error, startIndex, endIndex))

    candidates.sort(key=lambda c: c.errors)
    return candidates[:nCandidates]
