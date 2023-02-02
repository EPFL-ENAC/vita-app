"""Defines functions to generate preview image"""

from PIL import Image, ImageDraw, ImageFont
import os


# Define text style
fontPath = "ressources/Roboto-Regular.ttf"
textColor = (0, 0, 0)  # black

# Text area style
fill = (255, 255, 255, 192)  # semi-transparent white
lineWidth = 3
textOutline = (192, 0, 0)  # dark red
regionOutline = (192, 192, 192)  # light grey
defaultFontSize = 12


def toPixels(point, im):
    """Conversion helper function

    Args:
        point (Point): Object with coordinates ranging from 0 to 1
        im (Image)

    Returns:
        (Double, Double): Tuple of coordinates (in pixels)
    """
    return (
        point.x * im.width,
        (1 - point.y) * im.height,
    )  # inverted vertical axis


def generateFromOcrData(
    picturePath, detectedTextList, regions=[], verbose=False
):
    # Load cropped picture
    im = Image.open(picturePath)

    # Create draw object
    draw = ImageDraw.Draw(im, "RGBA")

    for region in regions:
        points = [toPixels(p, im) for p in region.points]
        draw.polygon(points, outline=regionOutline, width=lineWidth)

    for detectedText in detectedTextList:
        points = [toPixels(p, im) for p in detectedText.points]
        textPos = points[3]  # topLeft
        # middle vertical ahchor
        textPos = (
            textPos[0],
            textPos[1] + detectedText.lineHeight / 2 * im.height,
        )

        # Compute font size to fit drawn text width in bounding box
        font = ImageFont.truetype(fontPath, defaultFontSize)
        width, _ = font.getsize(detectedText.text)
        if width != 0:
            fontSize = round(
                defaultFontSize * detectedText.textWidth * im.width / width
            )
        else:
            fontSize = defaultFontSize
        font = ImageFont.truetype(fontPath, fontSize)

        draw.polygon(points, outline=textOutline, width=lineWidth, fill=fill)
        draw.text(
            textPos, detectedText.text, fill=textColor, font=font, anchor="lm"
        )

        bboxDebug = [
            f"({p.x:.3f}, {p.y:.3f})" for p in detectedText.bbox.points
        ]
        if verbose:
            print(f'drawing "{detectedText.text}" at', *bboxDebug)

    return im


def show(im):
    im.show()


def save(im, path):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    im.save(path)
    print(f"Image saved to {path}")
