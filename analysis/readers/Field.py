class Field:
    """Fields looked for by Readers

    Attributes:
        name (str): field identifier
        pattern (str): regular expression to match
        keys (list): name of data entries captured by pattern
            If empty, field can still be used to find other relative fields
        dataOrder ([int]|None): order in which keys should be reordered

        region (BoundingBox|None): region in which to look for pattern

        onRightof (str|None): name of relatively positioned field
        regionWidth (float|None): only used if onRightof is set

        below (str|None): name of relatively positioned field
        regionHeight (float): only used if below is set

        relativeTo (str|None): name of relatively positioned field
        regionRelative (BoundingBox|None): only used if relativeTo is set

        nCandidates (int): number of candidates to search
    """
    def __init__(
        self,
        name,
        pattern,
        keys=[],
        dataOrder=None,
        region=None,
        onRightof=None,
        regionWidth=None,
        below=None,
        regionHeight=1,
        relativeTo=None,
        regionRelative=None,
        nCandidates=None,
    ):
        self.name = name
        self.pattern = pattern
        self.keys = keys
        self.keysCaptureIds = dataOrder
        self.region = region
        self.onRightof = onRightof
        self.regionWidth = regionWidth
        self.below = below
        self.regionHeight = regionHeight
        self.relativeTo = relativeTo
        self.regionRelative = regionRelative
        self.nCandidates = nCandidates or 1
