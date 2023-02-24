import os

from models import detected_text
from reader_scripts.find_best_reader import find_best_reader
from reader_scripts.list_of_readers import readers
from utils import csv_writer
from utils import image_management as imgm
from utils.get_list_of_json_paths import get_list_of_json_paths


def gen_struct_out(args):
    if not args.display_images and args.output_dir is None:
        print("No output method specified. Use -d or -o.")
        quit()

    if args.software is not None:
        desired_reader = readers[args.software]
    else:
        desired_reader = None

    input_paths = get_list_of_json_paths(args.path, remove_extension=True)
    print(f"Found {len(input_paths)} .json files:")
    for filename in input_paths:
        print(f"{filename}.json")
    print("")

    # Loop through all the .json files
    for input_path in input_paths:
        process_file(input_path, args, desired_reader)


def process_file(input_path, args, desired_reader):
    print(f"Processing {input_path}")

    # Import detected text from OCR output
    all_detected_text = detected_text.gen_list_from_file(f"{input_path}.json")

    # Define used reader
    if desired_reader is not None:
        reader = desired_reader
    else:
        # Find best reader for this file
        reader = find_best_reader(all_detected_text)
        if reader is None:
            print(f"Could not find a matching reader for {input_path}")
            return

    # Generate structured output
    data, filtered_detected_text, regions = reader.read(all_detected_text)

    # Generate image with detected text
    if args.generate_images or args.display_images:
        im = imgm.generate_from_ocr_data(
            f"{input_path}.png",
            filtered_detected_text,
            regions,
            verbose=args.verbose,
        )
    else:
        im = None

    # Show image
    if args.display_images:
        imgm.show(im)

    # Save
    if args.output_dir is not None:
        output_path = os.path.join(args.output_dir, input_path)
        if im is not None:
            imgm.save(im, f"{output_path}_filtered.png")
        csv_writer.write(data, f"{output_path}.csv")

    # Print data
    if args.verbose:
        print("\nExtracted data:")
        for d in data:
            print(f"{list(d.keys())[0]}: {list(d.values())[0]}")
