"""Defines functions to generate preview image"""

import os

from PIL import Image, ImageDraw, ImageFont

# Define text style
font_path = "ressources/roboto_regular.ttf"
text_color = (0, 0, 0)  # black

# Text area style
fill = (255, 255, 255, 192)  # semi-transparent white
line_width = 3
text_outline = (192, 0, 0)  # dark red
region_outline = (192, 192, 192)  # light grey
default_font_size = 12


def to_pixels(point, im):
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


def generate_from_ocr_data(
    orig_picture_path, detected_text_list, regions=[], verbose=False
):
    # Load cropped picture
    im = Image.open(orig_picture_path)

    # Create draw object
    draw = ImageDraw.Draw(im, "RGBA")

    draw_regions(im, draw, regions)
    draw_detected_texts(im, draw, detected_text_list, verbose)

    return im


def draw_regions(im, draw, regions):
    for region in regions:
        points = [to_pixels(p, im) for p in region.points]
        draw.polygon(points, outline=region_outline, width=line_width)


def draw_detected_texts(im, draw, detected_text_list, verbose=False):
    for detected_text in detected_text_list:
        text_pos, box_points = compute_text_and_box_pos(im, detected_text)
        font = compute_sized_font(im, detected_text)

        draw.polygon(
            box_points, outline=text_outline, width=line_width, fill=fill
        )
        draw.text(
            text_pos,
            detected_text.text,
            fill=text_color,
            font=font,
            anchor="lm",
        )

        if verbose:
            bbox_debug = [
                f"({p.x:.3f}, {p.y:.3f})" for p in detected_text.bbox.points
            ]
            print(f'drawing "{detected_text.text}" at', *bbox_debug)


def compute_text_and_box_pos(im, detected_text):
    box_points = [to_pixels(p, im) for p in detected_text.points]
    text_pos = box_points[3]  # topLeft
    # middle vertical ahchor
    text_pos = (
        text_pos[0],
        text_pos[1] + detected_text.line_height / 2 * im.height,
    )
    return text_pos, box_points


def compute_sized_font(im, detected_text):
    """Compute font size to fit drawn text width in bounding box"""
    # Compute text width with default font size, then find new font size to
    # corretly rescale the text width
    font_temp = ImageFont.truetype(font_path, default_font_size)
    width, _ = font_temp.getsize(detected_text.text)
    if width != 0:
        font_size = round(
            default_font_size * detected_text.text_width * im.width / width
        )
    else:
        font_size = default_font_size
    font = ImageFont.truetype(font_path, font_size)
    return font


def show(im):
    im.show()


def save(im, path):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    im.save(path)
    print(f"Image saved to {path}")
