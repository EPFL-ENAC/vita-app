"""Defines functions to generate preview image"""

import os

from PIL import Image, ImageDraw, ImageFont

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

    Note that the origin is at the top left corner of the image (y axis must
    be inverted).

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
    origPicturePath, detectedTextList, regions=[], verbose=False
):
    # Load cropped picture
    im = Image.open(origPicturePath)

    # Create draw object
    draw = ImageDraw.Draw(im, "RGBA")

    drawRegions(im, draw, regions)
    drawDetectedTexts(im, draw, detectedTextList, verbose)

    return im


def drawRegions(im, draw, regions):
    for region in regions:
        points = [toPixels(p, im) for p in region.points]
        draw.polygon(points, outline=regionOutline, width=lineWidth)


def drawDetectedTexts(im, draw, detectedTextList, verbose=False):
    for detectedText in detectedTextList:
        textPos, boxPoints = computeTextAndBoxPos(im, detectedText)
        font = computeSizedFont(im, detectedText)

        draw.polygon(
            boxPoints, outline=textOutline, width=lineWidth, fill=fill
        )
        draw.text(
            textPos, detectedText.text, fill=textColor, font=font, anchor="lm"
        )

        if verbose:
            bboxDebug = [
                f"({p.x:.3f}, {p.y:.3f})" for p in detectedText.bbox.points
            ]
            print(f'drawing "{detectedText.text}" at', *bboxDebug)


def computeTextAndBoxPos(im, detectedText):
    boxPoints = [toPixels(p, im) for p in detectedText.points]
    textPos = boxPoints[3]  # topLeft
    # middle vertical ahchor
    textPos = (
        textPos[0],
        textPos[1] + detectedText.lineHeight / 2 * im.height,
    )
    return textPos, boxPoints


def computeSizedFont(im, detectedText):
    """Compute font size to fit drawn text width in bounding box"""
    # Compute text width with default font size, then find new font size to
    # corretly rescale the text width
    fontTemp = ImageFont.truetype(fontPath, defaultFontSize)
    width, _ = fontTemp.getsize(detectedText.text)
    if width != 0:
        fontSize = round(
            defaultFontSize * detectedText.textWidth * im.width / width
        )
    else:
        fontSize = defaultFontSize
    font = ImageFont.truetype(fontPath, fontSize)
    return font


def show(im):
    im.show()


def save(im, path):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    im.save(path)
    print(f"Image saved to {path}")
