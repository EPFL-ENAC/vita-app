import config
from readers.lists import formats
from readerScripts import search


def findBestReader(detectedTextList):
    bestError = config.ERROR_MAX + 1
    bestReader = None

    for format in formats:
        candidates = search.string(detectedTextList, format.distinctivePattern)
        if len(candidates) == 0:
            continue
        if candidates[0].errors < bestError:
            bestError = candidates[0].errors
            bestReader = format.reader

    if bestReader is not None:
        print(f"Best matching reader: {bestReader.name}")

    return bestReader
