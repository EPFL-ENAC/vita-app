class Candidate:
    """Container for DetectedText instance and fuzzySearch result"""

    def __init__(self, detectedText, errors, regexMatch, regionSearched=None):
        self.detectedText = detectedText
        self.errors = errors
        self.regexMatch = regexMatch
        self.regionSearched = regionSearched
