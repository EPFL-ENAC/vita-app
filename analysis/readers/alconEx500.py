import regex
from readers import search
from BoundingBox import BoundingBox


distinctivePattern = "EX500.+Treatment Report"

datePattern = r"\d{2}?\.\d{2}?\.\d{4}?"
timePattern = r"\d{2}?:\d{2}?:\d{2}?"
dateTimePattern = f"{datePattern} {timePattern}"


def read(detectedTextList):
    data = []

    # Name
    # Birth date
    # Eye (OS/OD)
    c = search.string(detectedTextList, "O[SD]", BoundingBox.fromBounds(0.2, 0.7, 0.7, 1))
    if len(c) != 0:
        data.append({ "eye": c[0].regexMatch.captures()[0] })

    # Gender
    # Treatment date
    c = search.string(detectedTextList, "Treatment date", BoundingBox.fromBounds(0.5, 1, 0.7, 1))
    if len(c) != 0:
        c = search.stringOnRight(c[0], detectedTextList, dateTimePattern, 10)
        if c is not None:
            data.append({ "Treatment date": c.regexMatch.captures()[0] })


    print(data)

    filteredDetectedText = detectedTextList
    return data, filteredDetectedText
