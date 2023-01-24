import sys
import DetectedText
import image
from readers.findBestReader import findBestReader
import csvWriter


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

# Check that input correcponds to Alcon EX500 format
reader = findBestReader(allDetectedText)
if reader is None:
    print("Could not find a matching reader.")
    quit()

# Generate structured output
data, filteredDetectedText = reader.read(allDetectedText)
csvWriter.write(data, f"{filename}.csv".replace("inputs/", "outputs/"))

# Show output
image.generate(f"{filename}.png", filteredDetectedText)

print("\nExtracted data:")
for d in data:
    print(f"{list(d.keys())[0]}: {list(d.values())[0]}")
