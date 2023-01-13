import DetectedText
import image


allDetectedText = DetectedText.fromFile("inputs/detectedText.json")
image.generate("inputs/cropped.png", allDetectedText)
