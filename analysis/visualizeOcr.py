import sys
import DetectedText
import image


if len(sys.argv) != 2:
    print("\nUsage: python3 structuredOutput.py path_to_json")
    quit()

filename = sys.argv[1]
jsonIndex = filename.find(".json")
if jsonIndex == -1:
    print("\nError: specified file is not a json")
    quit()

filename = filename[:jsonIndex]


# import from iOS output
allDetectedText = DetectedText.fromFile(f"{filename}.json")

# Show image
image.generate(f"{filename}.png", allDetectedText)
