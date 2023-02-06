import config
from readerScripts import search
from readerScripts.listOfReaders import readers


def findBestReader(detectedTextList):
    bestError = config.ERROR_MAX + 1
    bestReader = None

    for reader in list(readers.values()):
        candidates = search.searchString(
            detectedTextList, reader.distinctivePattern
        )
        if len(candidates) == 0:
            continue
        if candidates[0].errors < bestError:
            bestError = candidates[0].errors
            bestReader = reader

    if bestReader is not None:
        print(f"Best matching reader: {bestReader.name}")

    return bestReader
