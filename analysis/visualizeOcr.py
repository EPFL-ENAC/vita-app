import sys
from utils import getListOfJsonFilenames
import DetectedText
import image


if len(sys.argv) != 2:
    print("\nUsage: python3 structuredOutput.py path_to_json\n")
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

    # Generate image with detected text
    im = image.generate(f"{filename}.png", allDetectedText)
    image.save(im, f"{outname}_all.png")

    # Show image only if one file is processed
    if len(filenames) == 1:
        image.show(im)
