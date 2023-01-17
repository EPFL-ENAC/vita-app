import regex
import config
from readers import search
from BoundingBox import BoundingBox


distinctivePattern = "EX500.+Treatment Report"

namePattern = r"([a-zA-z\- ]+)"
datePattern = r"(\d{2}?\.\d{2}?\.\d{4}?)"
timePattern = r"(\d{2}?:\d{2}?:\d{2}?)"
dateTimePattern = f"{datePattern} {timePattern}"
anglePattern = r"(\d{1,3}) °"

shapeSpherePattern = r"([+-] \d+\.\d{2}) D"
shapeCylinderPattern = shapeSpherePattern
shapeAxisPattern = anglePattern
shapePattern = f"{shapeSpherePattern} {shapeCylinderPattern} x {shapeAxisPattern}"

lengthMmPattern = r"(\d+\.\d{2}) mm"
lengthUmPattern = r"(\d{1,4}) [up]m"
timeSPattern = r"(\d{1,3}) [sS]"

KPattern = r"(\d+\.\d{2}) D"
KAxisPattern = anglePattern
QPattern = r"([+-]?\d+\.\d{2}|-+)"
KQPattern = f"{KPattern} @ {KAxisPattern} / {QPattern}"


def searchData(keys, searchFunc, *args, **kwargs):
    newData = []
    errors = config.ERROR_MAX

    c = searchFunc(*args, **kwargs)

    if len(c) != 0:
        errors = c[0].errors

        # Fuzzy search always capture the whole pattern -> 1st group
        matches = list(c[0].regexMatch.groups())

        if len(matches) > 1:  # Other groups captured, get rid of 1st (whole)
            matches = matches[1:]

    else:  # no match found
        matches = [""] * len(keys)

    # Populate newData
    for i in range(len(keys)):
        newData.append({keys[i]: matches[i]})

    return newData, errors


def searchDataRelative(references, keys, searchFunc, *args, **kwargs):
    newData = [{key: ""} for key in keys]
    errors = config.ERROR_MAX

    if len(references) == 0:  # reference not found
        return newData, errors

    # Test all references to find which one leads to best match
    bestNewData = newData
    bestErrors = errors + 1

    for reference in references:
        newData, errors = searchData(keys, searchFunc, reference, *args, **kwargs)
        if errors < bestErrors:
            bestNewData = newData
            bestErrors = errors

    return bestNewData, bestErrors


def read(detectedTextList):
    data = []

    # Name
    refs = search.string(detectedTextList, distinctivePattern)
    data.extend(
        searchDataRelative(
            refs,
            ["Last name", "First name"],
            search.stringBelow,
            detectedTextList,
            f"{namePattern}, {namePattern}",
        )[0]
    )

    # Birth date
    data.extend(
        searchDataRelative(
            refs,
            ["Birth date"],
            search.stringBelow,
            detectedTextList,
            datePattern,
        )[0]
    )

    # Gender
    refs = search.string(detectedTextList, "Gender")
    data.extend(
        searchDataRelative(
            refs,
            ["Gender"],
            search.stringOnRight,
            detectedTextList,
            r"[a-z]*",
            10,
        )[0]
    )

    # Eye (OS/OD)
    data.extend(
        searchData(
            ["eye"],
            search.string,
            detectedTextList,
            "O[SD]",
            BoundingBox.fromBounds(0.2, 0.7, 0.7, 1),
        )[0]
    )

    # Treatment date
    refs = search.string(
        detectedTextList, "Treatment date", BoundingBox.fromBounds(0.5, 1, 0.7, 1)
    )
    data.extend(
        searchDataRelative(
            refs,
            ["Treatment date (DD.MM.YYYY)", "Treatment time"],
            search.stringOnRight,
            detectedTextList,
            dateTimePattern,
            10,
        )[0]
    )

    # Refraction
    refs = search.string(detectedTextList, "Refraction")
    data.extend(
        searchDataRelative(
            refs,
            ["Refraction sphere", "Refraction cylinder", "Refraction axis"],
            search.stringOnRight,
            detectedTextList,
            shapePattern,
            20,
        )[0]
    )

    # Treatment
    refs = search.string(detectedTextList, "(Treatment|Correction)", nCandidates=5)
    data.extend(
        searchDataRelative(
            refs,
            ["Treatment sphere", "Treatment cylinder", "Treatment axis"],
            search.stringOnRight,
            detectedTextList,
            shapePattern,
            20,
        )[0]
    )

    # Optical zone
    refs = search.string(detectedTextList, "Optical zone")
    data.extend(
        searchDataRelative(
            refs,
            ["Optical zone"],
            search.stringOnRight,
            detectedTextList,
            lengthMmPattern,
            5,
        )[0]
    )

    # Flap / Epi Thickness
    refs = search.string(detectedTextList, "(Flap / Epi Thickness|Planned flap)")
    data.extend(
        searchDataRelative(
            refs,
            ["Flap / Epi thickness"],
            search.stringOnRight,
            detectedTextList,
            lengthUmPattern,
            5,
        )[0]
    )

    # Transition zone
    refs = search.string(detectedTextList, "Transition zone")
    data.extend(
        searchDataRelative(
            refs,
            ["Transition zone"],
            search.stringOnRight,
            detectedTextList,
            lengthMmPattern,
            5,
        )[0]
    )

    # Cornea thickness
    refs = search.string(detectedTextList, "Cornea thickness")
    data.extend(
        searchDataRelative(
            refs,
            ["Cornea thickness"],
            search.stringOnRight,
            detectedTextList,
            lengthUmPattern,
            5,
        )[0]
    )

    # Ablation zone
    refs = search.string(detectedTextList, "Ablation zone")
    data.extend(
        searchDataRelative(
            refs,
            ["Ablation zone"],
            search.stringOnRight,
            detectedTextList,
            lengthMmPattern,
            5,
        )[0]
    )

    # Residual stroma
    refs = search.string(detectedTextList, "Residual stroma")
    data.extend(
        searchDataRelative(
            refs,
            ["Residual stroma"],
            search.stringOnRight,
            detectedTextList,
            lengthUmPattern,
            5,
        )[0]
    )

    # Total duration
    refs = search.string(detectedTextList, "Total duration")
    data.extend(
        searchDataRelative(
            refs,
            ["Total duration (s)"],
            search.stringOnRight,
            detectedTextList,
            timeSPattern,
            5,
        )[0]
    )

    # Breaks
    refs = search.string(detectedTextList, "Breaks")
    data.extend(
        searchDataRelative(
            refs,
            ["Breaks (s)"],
            search.stringOnRight,
            detectedTextList,
            rf"\d+ \({timeSPattern}\)",
            5,
        )[0]
    )

    # K1 / Q1
    refs = search.string(detectedTextList, "K1 / Q1")
    data.extend(
        searchDataRelative(
            refs,
            ["K1", "K1 axis", "Q1"],
            search.stringOnRight,
            detectedTextList,
            KQPattern,
            20,
        )[0]
    )

    # K2 / Q2
    refs = search.string(detectedTextList, "K2 / Q2")
    data.extend(
        searchDataRelative(
            refs,
            ["K2", "K2 axis", "Q2"],
            search.stringOnRight,
            detectedTextList,
            KQPattern,
            20,
        )[0]
    )

    # Pupil
    refs = search.string(detectedTextList, "Pupil")
    data.extend(
        searchDataRelative(
            refs,
            ["Pupil"],
            search.stringOnRight,
            detectedTextList,
            lengthMmPattern,
            5,
        )[0]
    )

    print(data)

    filteredDetectedText = detectedTextList
    return data, filteredDetectedText
