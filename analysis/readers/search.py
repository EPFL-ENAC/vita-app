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
        regexMatch (Match)
    """
    regexPattern = f"({pattern}){{e<={errorMax}}}"
    match = regex.search(regexPattern, string, regex.BESTMATCH)

    if match is None:
        return None, None

    # match.fuzzy_counts: (n_substitutions, n_insertions, n_deletes)
    errors = sum(match.fuzzy_counts)

    return errors, match


class Candidate:
    """Container for DetectedText instance and fuzzySearch result"""

    def __init__(self, detectedText, errors, regexMatch):
        self.detectedText = detectedText
        self.errors = errors
        self.regexMatch = regexMatch


def string(detectedTextList, pattern, region=None, nCandidates=1):
    """Searches for a string in all provided detected texts

    Args
        detectedTextList ([detectedText])
        pattern (string): regex pattern
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

        error, regexMatch = fuzzySearch(
            pattern, detectedText.text, config.ERROR_MAX
        )

        if error is None:
            continue

        candidates.append(Candidate(detectedText, error, regexMatch))

    candidates.sort(key=lambda c: c.errors)
    return candidates[:nCandidates]


def stringOnRight(reference, detectedTextList, pattern, regionWidth=0):
    """Searches for a string on the right of a reference

    The checked region includes the reference bounding box, in case the
    searched string is inside the reference.

    Args:
        reference (detectedText)
        detectedTextList ([detectedText])
        pattern (string): regex pattern
        regionWidth (float): width added to the reference bounding box where
            text is searched. added width = reference.lineHeight * regionWidth

    Returns:
        candidate
    """

    # Create searched region by expanding the reference's bounding box
    region = reference.bbox.copy()
    addedWidth = regionWidth * reference.lineHeight
    region.bottomRight.x += addedWidth
    region.topRight.x += addedWidth

    candidates = string(detectedTextList, pattern, region)
    return candidates[0] if len(candidates) != 0 else None


def stringBelow(reference, detectedTextList, pattern):
    """Searches for a string below a reference

    The checked region is the reference bounding box shifted down by one
    lineHeight.

    Args:
        reference (detectedText)
        detectedTextList ([detectedText])
        pattern (string): regex pattern

    Returns:
        candidate
    """

    # Create searched region by shifting the reference's bounding box down
    region = reference.bbox.copy()
    for p in region.points:
        p.y -= reference.lineHeight

    candidates = string(detectedTextList, pattern, region)
    return candidates[0] if len(candidates) != 0 else None
