import sys
import DetectedText
import image


if len(sys.argv) != 2:
    print("\nUsage: python3 structuredOutput.py filename")
    print('filename: name of files in "input/" directory without extension')
    quit()

filename = sys.argv[1]


# import from iOS output
allDetectedText = DetectedText.fromFile(f"inputs/{filename}.json")

# Show image
image.generate(f"inputs/{filename}.png", allDetectedText)
