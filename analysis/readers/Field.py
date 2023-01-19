class Field:
    def __init__(
        self,
        name,
        pattern,
        keys=None,
        region=None,
        onRightof=None,
        regionWidth=None,
        below=None,
        nCandidates=None,
    ):
        self.name = name
        self.pattern = pattern
        self.keys = keys
        self.region = region
        self.onRightof = onRightof
        self.regionWidth = regionWidth  # only used if onRightof is set
        self.below = below
        self.nCandidates = nCandidates or 1
