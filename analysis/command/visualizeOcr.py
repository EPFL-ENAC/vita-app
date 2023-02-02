from utils import getListOfJsonPaths
import os
import DetectedText
import image


def visualizeOcr(args):
    if not args.display_images and args.output_dir is None:
        print("No output method specified. Use -d or -o.")
        quit()

    inputPaths = getListOfJsonPaths(args.path)

    # Loop through all the .json files
    for inputPath in inputPaths:
        processFile(inputPath, args)


def processFile(inputPath, args):
    print(f"Processing {inputPath}")

    # Import detected text from OCR output
    allDetectedText = DetectedText.fromFile(f"{inputPath}.json")

    # Generate image with detected text
    im = image.generateFromOcrData(
        f"{inputPath}.png", allDetectedText, verbose=args.verbose
    )

    # Save image
    if args.output_dir is not None:
        outputPath = os.path.join(args.output_dir, inputPath)
        image.save(im, f"{outputPath}_all.png")

    # Show image
    if args.display_images:
        image.show(im)
