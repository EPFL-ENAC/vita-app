import sys
import DetectedText
import image
from readers import alconEx500, search
import csvWriter


if len(sys.argv) != 2:
    print("\nUsage: python3 structuredOutput.py filename")
    print('filename: name of files in "input/" directory without extension')
    quit()

filename = sys.argv[1]


# import from iOS output
allDetectedText = DetectedText.fromFile(f"inputs/{filename}.json")

# Check that input correcponds to Alcon EX500 format
candidates = search.string(allDetectedText, alconEx500.distinctivePattern)
if len(candidates) != 1:
    print("Error: input does not correspond to Alcon EX500 format.")
    quit()

data, filteredDetectedText = alconEx500.reader.read(allDetectedText)
csvWriter.write(data, f"outputs/{filename}.csv")

image.generate(f"inputs/{filename}.png", filteredDetectedText)
print(data)
