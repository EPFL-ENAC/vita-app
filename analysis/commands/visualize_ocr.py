import os

from utils import image_management as imgm
from utils.get_detected_text_from_json import get_detected_text_from_json
from utils.get_list_of_json_paths import get_list_of_json_paths


def visualize_ocr(args):
    if not args.display_images and args.output_dir is None:
        print("No output method specified. Use -d or -o.")
        quit()

    input_paths = get_list_of_json_paths(args.path, remove_extension=True)
    print(f"Found {len(input_paths)} .json files:")
    for filename in input_paths:
        print(f"{filename}.json")
    print("")

    # Loop through all the .json files
    for input_path in input_paths:
        process_file(input_path, args)


def process_file(input_path, args):
    print(f"Processing {input_path}")

    # Import detected text from OCR output
    detected_text_list = get_detected_text_from_json(f"{input_path}.json")

    # Generate image with detected text
    im = imgm.generate_from_ocr_data(
        f"{input_path}.jpg", detected_text_list, verbose=args.verbose
    )

    # Save image
    if args.output_dir is not None:
        output_path = os.path.join(
            args.output_dir, os.path.basename(input_path)
        )
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        imgm.save(im, f"{output_path}_all.jpg")

    # Show image
    if args.display_images:
        imgm.show(im)
