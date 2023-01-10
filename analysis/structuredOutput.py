import json
from PIL import Image, ImageDraw, ImageFont

POINT_NAMES = ["bottomLeft", "bottomRight", "topRight", "topLeft"]


# Read JSON input
f = open("inputs/detectedText.json")
data = json.load(f)
f.close()


# Load cropped picture
im = Image.open("inputs/cropped.png")

# Create draw object
draw = ImageDraw.Draw(im, "RGBA")

# Define text style
fontPath = "ressources/Roboto-Regular.ttf"
textColor = (0, 0, 0) # black

# Text area style
fill = (255, 255, 255, 192) # semi-transparent white
lineWidth = 3
outline = (192, 0, 0) # dark red

# convertion helper function
def pointFromData(data):
	return (
		data["x"] * im.width,
		(1 - data["y"]) * im.height # inverted vertical axis
	)

for detectedText in data:
	text = detectedText["text"]
	points = [pointFromData(detectedText["bbox"][name]) for name in POINT_NAMES]
	textPos = points[3] # topLeft

	fontSize = round(points[0][1] - points[3][1]) # height if bbox, in pixels
	if fontSize < 0: fontSize = 0
	font = ImageFont.truetype(fontPath, fontSize) # TODO: change arbitrary font size

	draw.polygon(points, outline=outline, width=lineWidth, fill=fill)
	draw.text(textPos, text, fill=textColor, font=font)
	print(text)
	
im.show()

