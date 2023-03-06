from models.bounding_box import BoundingBox
from models.crop_region import CropRegion
from models.cropped_ocr_results import CroppedOcrResults
from models.detected_text import DetectedText


def test_get_absolute_coordinates():
    x_crop = 0.1
    y_crop = 0.2
    width_crop = 0.3
    height_crop = 0.4
    crop_region = CropRegion(x_crop, y_crop, width_crop, height_crop)

    cropped_ocr_results = CroppedOcrResults(crop_region)

    xmin_text = 0.5
    xmax_text = 0.6
    ymin_text = 0.7
    ymax_text = 0.8
    bbox_text = BoundingBox.from_bounds(
        xmin_text, xmax_text, ymin_text, ymax_text
    )
    detected_text = DetectedText("text", bbox_text)
    cropped_ocr_results.detected_text_list.append(detected_text)

    absolute_detected_text_list = (
        cropped_ocr_results.get_absolute_detected_text_list()
    )
    absolute_bbox = absolute_detected_text_list[0].bbox
    xmin_absolute = x_crop + width_crop * xmin_text
    xmax_absolute = x_crop + width_crop * xmax_text
    ymin_absolute = y_crop + height_crop * ymin_text
    ymax_absolute = y_crop + height_crop * ymax_text

    assert absolute_bbox.bottom_left.x == xmin_absolute
    assert absolute_bbox.bottom_left.y == ymin_absolute
    assert absolute_bbox.top_right.x == xmax_absolute
    assert absolute_bbox.top_right.y == ymax_absolute
