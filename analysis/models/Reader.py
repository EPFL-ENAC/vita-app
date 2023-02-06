import config
from models.Field import FieldBelow, FieldOnRight, FieldRelative, fieldFromConf
from readerScripts import search


class Reader:
    def __init__(self, conf):
        self.name = conf["name"]
        self.distinctivePattern = conf["distinctivePattern"]
        self.fields = []

        for fieldConf in conf["fields"]:
            self.fields.append(fieldFromConf(fieldConf))

    def read(self, detectedTextList):
        """Build data from detected texts"""

        filteredDetectedText = set()
        fieldCandidates = {}
        data = []
        regions = []

        for field in self.fields:
            # Extract data and candidates
            newData, bestRef, candidates = getDataFromField(
                field, fieldCandidates, detectedTextList
            )

            # Populate filteredDetectedText
            for candidate in candidates:
                if candidate.detectedText not in detectedTextList:
                    continue
                filteredDetectedText.add(candidate.detectedText)

            if bestRef is not None:
                if bestRef.detectedText in detectedTextList:
                    filteredDetectedText.add(bestRef.detectedText)

            # Save region where field was shearched
            if len(candidates) > 0:
                region = candidates[0].regionSearched
                if region is not None:
                    regions.append(region)

            # Save field candidates
            fieldCandidates[field.name] = candidates

            # If no keys provided, no need to save data
            if len(field.keys) == 0:
                continue

            # Reorder data if needed
            if field.keysCaptureIds is not None:
                newData = [newData[i] for i in field.keysCaptureIds]

            data.extend(newData)

        return data, list(filteredDetectedText), regions


def getDataFromField(field, fieldCandidates, detectedTextList):
    if isinstance(field, FieldOnRight):
        refs = fieldCandidates[field.onRightof]
        newData, bestRef, candidates, _ = searchDataRelative(
            refs,
            field.keys,
            search.searchStringOnRight,
            detectedTextList,
            field.pattern,
            field.regionWidth,
            field.nCandidates,
        )

    elif isinstance(field, FieldBelow):
        refs = fieldCandidates[field.below]
        newData, bestRef, candidates, _ = searchDataRelative(
            refs,
            field.keys,
            search.searchStringBelow,
            detectedTextList,
            field.pattern,
            field.regionHeight,
            field.nCandidates,
        )

    elif isinstance(field, FieldRelative):
        refs = fieldCandidates[field.relativeTo]
        newData, bestRef, candidates, _ = searchDataRelative(
            refs,
            field.keys,
            search.searchStringRelative,
            detectedTextList,
            field.pattern,
            field.regionRelative,
            nCandidates=field.nCandidates,
            includeReference=True,
        )

    else:  # Non-relative field
        bestRef = None
        newData, candidates, _ = searchData(
            field.keys,
            search.searchString,
            detectedTextList,
            field.pattern,
            field.region,
        )

    return newData, bestRef, candidates


def searchData(keys, searchFunc, *args, **kwargs):
    """Searches a string and builds corresponding data

    Args:
        keys ([string]): keys of the data to build
        searchFunc (function): function to use to search the string
        *args: arguments passed to searchFunc
        **kwargs: keyword arguments passed to searchFunc

    Returns:
        newData ([{key: string}]): data built from the search
        candidates ([Candidate]): candidates found by searchFunc
        errors (int): number of errors in the best match
    """

    newData = []
    errors = config.ERROR_MAX

    candidates = searchFunc(*args, **kwargs)

    # Build list of values corresponding to each key
    if len(candidates) != 0:
        errors = candidates[0].errors

        matches = list(candidates[0].regexMatch.groups())

        # Fuzzy search function always capture the whole pattern in 1st group
        if len(matches) > 1:  # Other groups captured, get rid of 1st (whole)
            matches = matches[1:]

    else:  # no match found, empty values
        matches = [""] * len(keys)

    # Populate newData
    for i in range(len(keys)):
        newData.append({keys[i]: matches[i]})

    return newData, candidates, errors


def searchDataRelative(references, keys, searchFunc, *args, **kwargs):
    """Searches a string relative to a reference and builds corresponding data

    Args:
        references ([Candidate]): list of references to search relative to.
        keys ([string]): keys of the data to build
        searchFunc (function): function to use to search the string
        *args: arguments passed to searchFunc
        **kwargs: keyword arguments passed to searchFunc

    Returns:
        bestNewData ([{key: string}]): data built from the search
        bestReference (Candidate): reference that led to best match
        bestCandidates ([Candidate]): candidates found by searchFunc
        bestErrors (int): number of errors in the best match
    """

    newData = [{key: ""} for key in keys]
    errors = config.ERROR_MAX

    if len(references) == 0:  # reference not found
        return newData, None, [], errors

    # Test all references to find which one leads to best match
    bestNewData = newData
    bestReference = None
    bestCandidates = []
    bestErrors = errors + 1

    for reference in references:
        newData, candidates, errors = searchData(
            keys, searchFunc, reference, *args, **kwargs
        )
        if errors < bestErrors:
            bestNewData = newData
            bestReference = reference
            bestCandidates = candidates
            bestErrors = errors

    return bestNewData, bestReference, bestCandidates, bestErrors
