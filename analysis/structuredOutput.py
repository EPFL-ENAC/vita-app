import sys
from utils import getListOfJsonFilenames
import DetectedText
import image
from readers.findBestReader import findBestReader
import csvWriter


if len(sys.argv) != 2:
    print("\nUsage: python3 structuredOutput.py path_to_json")
    print("If path_to_json is a directory, all the json files in the directory tree will be processed.")
    quit()

filenames = getListOfJsonFilenames(sys.argv[1])


# Loop through all the json files
for filename in filenames:
    print(f"\nProcessing {filename}\n")

    # Remove .json extension
    filename = filename[:filename.rfind(".json")]
    outname = filename.replace("inputs/", "outputs/")

    # import from iOS output
    allDetectedText = DetectedText.fromFile(f"{filename}.json")

    # Check that input correcponds to Alcon EX500 format
    reader = findBestReader(allDetectedText)
    if reader is None:
        print(f"Could not find a matching reader for {filename}")
        continue

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
