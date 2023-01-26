import sys
import DetectedText
import image


if len(sys.argv) != 2:
    print("\nUsage: python3 visualizeOcr.py path_to_json")
    quit()

filename = sys.argv[1]
jsonIndex = filename.find(".json")
if jsonIndex == -1:
    print("\nError: specified file is not a json")
    quit()

# Remove .json extension
filename = filename[:jsonIndex]
outname = filename.replace("inputs/", "outputs/")


# import from iOS output
allDetectedText = DetectedText.fromFile(f"{filename}.json")

# Show image
im = image.generate(f"{filename}.png", allDetectedText)
image.save(im, f"{outname}_all.png")
