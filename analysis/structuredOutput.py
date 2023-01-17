import DetectedText
import image
from readers import alconEx500, search
import csvWriter


# import from iOS output
allDetectedText = DetectedText.fromFile("inputs/detectedText.json")

# Check that input correcponds to Alcon EX500 format
candidates = search.string(allDetectedText, alconEx500.distinctivePattern)
if len(candidates) != 1:
    print("Error: input does not correspond to Alcon EX500 format.")
    quit()

data, filteredDetectedText = alconEx500.read(allDetectedText)
csvWriter.write(data, "output.csv")

# image.generate("inputs/cropped.png", filteredDetectedText)
