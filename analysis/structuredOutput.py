import sys
import DetectedText
import image
from readers.findBestReader import findBestReader
import csvWriter


if len(sys.argv) != 2:
    print("\nUsage: python3 structuredOutput.py filename")
    print('filename: name of files in "input/" directory without extension')
    quit()

filename = sys.argv[1]


# import from iOS output
allDetectedText = DetectedText.fromFile(f"inputs/{filename}.json")

# Check that input correcponds to Alcon EX500 format
reader = findBestReader(allDetectedText)
if reader is None:
    print("Could not find a matching reader.")
    quit()

# Generate structured output
data, filteredDetectedText = reader.read(allDetectedText)
csvWriter.write(data, f"outputs/{filename}.csv")

# Show output
image.generate(f"inputs/{filename}.png", filteredDetectedText)

print("\nExtracted data:")
for d in data:
    print(f"{list(d.keys())[0]}: {list(d.values())[0]}")
