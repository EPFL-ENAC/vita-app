from models.BoundingBox import BoundingBox


class Field:
    """Field searched by Readers

    Attributes:
        name (str): field identifier
        pattern (str): regular expression to match
        region (BoundingBox|None): region in which to look for pattern. If
            None, field is searched in the whole image.
        keys (list): name of data entries captured by pattern.
            If empty, field can still be used to find other relative fields.
        dataOrder ([int]|None): order in which keys should be reordered
        nCandidates (int): number of candidates to search
    """

    def __init__(
        self,
        name,
        pattern,
        region=None,
        keys=[],
        dataOrder=None,
        nCandidates=None,
    ):
        self.name = name
        self.pattern = pattern
        self.region = region
        self.keys = keys
        self.keysCaptureIds = dataOrder
        self.nCandidates = nCandidates or 1


class FieldRelative(Field):
    """Field positioned relatively to another field

    Attributes:
        name (str): field identifier
        pattern (str): regular expression to match

        relativeTo (str): name of relatively positioned field
        regionRelative (BoundingBox): specified relative to reference's center
        and in units of reference's lineHeight

        keys (list): name of data entries captured by pattern.
            If empty, field can still be used to find other relative fields.
        dataOrder ([int]|None): order in which keys should be reordered
        nCandidates (int): number of candidates to search
    """

    def __init__(
        self,
        name,
        pattern,
        relativeTo,
        regionRelative,
        keys=[],
        dataOrder=None,
        nCandidates=None,
    ):
        super().__init__(
            name,
            pattern,
            keys=keys,
            dataOrder=dataOrder,
            nCandidates=nCandidates,
        )
        self.relativeTo = relativeTo
        self.regionRelative = regionRelative


class FieldOnRight(Field):
    """Field positioned on the right of another field

    Attributes:
        name (str): field identifier
        pattern (str): regular expression to match

        onRightof (str): name of the reference field
        regionWidth (float|None): width added to the reference bounding box
            where text is searched.
            Added width = reference.lineHeight * regionWidth.
            If None, search the whole srceen width.

        keys (list): name of data entries captured by pattern.
            If empty, field can still be used to find other relative fields.
        dataOrder ([int]|None): order in which keys should be reordered
        nCandidates (int): number of candidates to search
    """

    def __init__(
        self,
        name,
        pattern,
        onRightof,
        regionWidth=None,
        keys=[],
        dataOrder=None,
        nCandidates=None,
    ):
        super().__init__(
            name,
            pattern,
            keys=keys,
            dataOrder=dataOrder,
            nCandidates=nCandidates,
        )
        self.onRightof = onRightof
        self.regionWidth = regionWidth


class FieldBelow(Field):
    """Field positioned below another field

    Attributes:
        name (str): field identifier
        pattern (str): regular expression to match

        below (str): name of the reference field
        regionHeight (float): height of the region where text is searched,
            in units of reference.lineHeight. A greater value extends the
            region downwards.

        keys (list): name of data entries captured by pattern.
            If empty, field can still be used to find other relative fields.
        dataOrder ([int]|None): order in which keys should be reordered
        nCandidates (int): number of candidates to search
    """

    def __init__(
        self,
        name,
        pattern,
        below,
        regionHeight=1.0,
        keys=[],
        dataOrder=None,
        nCandidates=None,
    ):
        super().__init__(
            name,
            pattern,
            keys=keys,
            dataOrder=dataOrder,
            nCandidates=nCandidates,
        )
        self.below = below
        self.regionHeight = regionHeight


def fieldFromConf(conf):
    conf = conf.copy()

    if "relativeTo" in conf:
        conf["regionRelative"] = BoundingBox.fromBounds(
            *conf["regionRelative"]
        )
        return FieldRelative(**conf)

    elif "onRightof" in conf:
        return FieldOnRight(**conf)

    elif "below" in conf:
        return FieldBelow(**conf)

    else:
        if "region" in conf:
            conf["region"] = BoundingBox.fromBounds(*conf["region"])
        return Field(**conf)
