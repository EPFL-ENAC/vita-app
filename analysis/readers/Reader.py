import config
from readers import search


class Reader:
    def __init__(self, name, distinctivePattern, fields):
        self.name = name
        self.distinctivePattern = distinctivePattern
        self.fields = fields

    def read(self, detectedTextList):
        """Bluid data from detected texts"""

        filteredDetectedText = set()
        fieldCandidates = {}
        data = []

        for field in self.fields:
            if field.onRightof is not None:
                refs = fieldCandidates[field.onRightof]
                newData, bestRef, candidates, _ = searchDataRelative(
                    refs,
                    field.keys,
                    search.stringOnRight,
                    detectedTextList,
                    field.pattern,
                    field.regionWidth,
                    field.nCandidates,
                )

            elif field.below is not None:
                refs = fieldCandidates[field.below]
                newData, bestRef, candidates, _ = searchDataRelative(
                    refs,
                    field.keys,
                    search.stringBelow,
                    detectedTextList,
                    field.pattern,
                    field.nCandidates,
                )

            elif field.relativeTo is not None:
                refs = fieldCandidates[field.relativeTo]
                newData, bestRef, candidates, _ = searchDataRelative(
                    refs,
                    field.keys,
                    search.stringRelative,
                    detectedTextList,
                    field.pattern,
                    field.regionRelative,
                    nCandidates=field.nCandidates,
                    includeReference=True
                )

            else:  # Non-relative field
                bestRef = None
                newData, candidates, _ = searchData(
                    field.keys,
                    search.string,
                    detectedTextList,
                    field.pattern,
                    field.region,
                )


            # Populate filteredDetectedText
            for candidate in candidates:
                if candidate.detectedText not in detectedTextList:
                    continue
                filteredDetectedText.add(candidate.detectedText)

            if bestRef is not None:
                filteredDetectedText.add(bestRef.detectedText)

            # Save field candidates
            fieldCandidates[field.name] = candidates

            # If no keys provided, no need to save data
            if len(field.keys) == 0:
                continue

            # Reorder data if needed
            if field.keysCaptureIds is not None:
                newData = [newData[i] for i in field.keysCaptureIds]

            data.extend(newData)

        return data, list(filteredDetectedText)


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
