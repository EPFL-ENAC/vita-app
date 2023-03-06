import json

from models.cropped_ocr_results import CroppedOcrResults


def get_detected_text_from_json(filename):
    # Read JSON input
    f = open(filename)
    data = json.load(f)
    f.close()

    cropped_ocr_results_list = []
    for d in data:
        cropped_ocr_results_list.append(CroppedOcrResults.from_data(d))

    detected_text_list = []

    for cropped_ocr_results in cropped_ocr_results_list:
        detected_text_list.extend(
            cropped_ocr_results.get_absolute_detected_text_list()
        )

    return detected_text_list
