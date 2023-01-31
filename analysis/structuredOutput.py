import sys
from utils import getListOfJsonFilenames
import DetectedText
import image
from readers.findBestReader import findBestReader
from readers.list import formats, names as formatNames, readers
import csvWriter


if len(sys.argv) != 2 and len(sys.argv) != 3:
    print("\nUsage: python3 structuredOutput.py path_to_json [format]\n")
    print("If path_to_json is a directory, all the json files in the directory tree will be processed.")
    print("If 'format' is not specified, the best format will be automatically selected. 'format' must be taken from the following list:")
    for name in formatNames:
        print(f'\t"{name}"')
    quit()

filenames = getListOfJsonFilenames(sys.argv[1])

if len(sys.argv) == 3:
    formatName = sys.argv[2]
    if formatName not in formatNames:
        print(f"Unknown reader: {formatName}")
        quit()
    desiredReader = readers[formatName]
else:
    desiredReader = None


# Loop through all the json files
for filename in filenames:
    print(f"\nProcessing {filename}\n")

    # Remove .json extension
    filename = filename[:filename.rfind(".json")]
    outname = filename.replace("inputs/", "outputs/")

    # import from iOS output
    allDetectedText = DetectedText.fromFile(f"{filename}.json")

    if desiredReader is None:
        # Find best reader
        reader = findBestReader(allDetectedText)
        if reader is None:
            print(f"Could not find a matching reader for {filename}")
            continue
    else:
        reader = desiredReader

    # Generate structured output
    data, filteredDetectedText = reader.read(allDetectedText)
    csvWriter.write(data, f"{outname}.csv")

    # Generate image with detected text
    im = image.generate(f"{filename}.png", filteredDetectedText)
    image.save(im, f"{outname}_filtered.png")

    # Show image only if one file is processed
    if len(filenames) == 1:
        image.show(im)

    # Print data
    print("\nExtracted data:")
    for d in data:
        print(f"{list(d.keys())[0]}: {list(d.values())[0]}")
