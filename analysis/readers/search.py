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
        region (BoundingBox | None): check if candidate bounding box's center
            is inside region
        nCandidates (int): number of candidates to return

    Returns:
        candidates ([Candidates]): nCandidates first candidates matching the
            pattern
    """

    candidates = []

    for detectedText in detectedTextList:
        if region is not None:
            center = detectedText.bbox.getBarycenter()
            if not region.contains(center):
                continue

        error, regexMatch = fuzzySearch(pattern, detectedText.text, config.ERROR_MAX)

        if error is None:
            continue

        candidates.append(Candidate(detectedText, error, regexMatch))

    candidates.sort(key=lambda c: c.errors)
    return candidates[:nCandidates]


def stringOnRight(reference, detectedTextList, pattern, regionWidth=0, nCandidates=1):
    """Searches for a string on the right of a reference

    The checked region includes the reference bounding box, in case the
    searched string is inside the reference.

    Args:
        reference (Candidate)
        detectedTextList ([detectedText])
        pattern (string): regex pattern
        regionWidth (float): width added to the reference bounding box where
            text is searched. added width = reference.lineHeight * regionWidth
        nCandidates (int): number of candidates to return

    Returns:
        candidates ([Candidates]): nCandidates first candidates. May return
            elements which are not originally in detectedTextList.
    """

    # Create searched region by expanding the reference's bounding box
    region = reference.detectedText.bbox.copy()
    addedWidth = regionWidth * reference.detectedText.lineHeight
    region.bottomRight.x += addedWidth
    region.topRight.x += addedWidth

    # Build modified detectedTextList not containing the full "reference"
    # text, which may contain a match before refEndIndex.
    # Example: reference text is "unwanted-value key: value", we should
    # prevent "unwanted-value" from matching.
    detectedTextList = detectedTextList.copy()  # don't mutate original list
    detectedTextList.remove(reference.detectedText)
    cropped = reference.detectedText.copy()
    cropped.text = cropped.text[reference.regexMatch.span()[1] :]
    detectedTextList.append(cropped)

    return string(detectedTextList, pattern, region, nCandidates)


def stringBelow(reference, detectedTextList, pattern, nCandidates=1):
    """Searches for a string below a reference

    The checked region is the reference bounding box shifted down by one
    lineHeight.

    Args:
        reference (Candidate)
        detectedTextList ([detectedText])
        pattern (string): regex pattern
        nCandidates (int): number of candidates to return

    Returns:
        candidates ([Candidates]): nCandidates first candidates
    """

    # Create searched region by shifting the reference's bounding box down
    region = reference.detectedText.bbox.copy()
    for p in region.points:
        p.y -= reference.detectedText.lineHeight

    return string(detectedTextList, pattern, region)
