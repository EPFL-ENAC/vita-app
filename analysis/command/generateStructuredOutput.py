from utils import getListOfJsonPaths
import DetectedText
import image
from readers.findBestReader import findBestReader
from readers.list import names as readers
import csvWriter
import os


def generateStructuredOutput(args):
    if not args.display_images and args.output_dir is None:
        print("No output method specified. Use -d or -o.")
        quit()

    if args.software is not None:
        desiredReader = readers[args.software]
    else:
        desiredReader = None

    inputPaths = getListOfJsonPaths(args.path)

    # Loop through all the .json files
    for inputPath in inputPaths:
        processFile(inputPath, args, desiredReader)


def processFile(inputPath, args, desiredReader):
    print(f"Processing {inputPath}")

    # Import detected text from OCR output
    allDetectedText = DetectedText.fromFile(f"{inputPath}.json")

    # Define used reader
    if desiredReader is None:
        # Find best reader
        reader = findBestReader(allDetectedText)
        if reader is None:
            print(f"Could not find a matching reader for {inputPath}")
            return
    else:
        reader = desiredReader

    # Generate structured output
    data, filteredDetectedText, regions = reader.read(allDetectedText)

    # Generate image with detected text
    if args.generate_images or args.display_images:
        im = image.generateFromOcrData(
            f"{inputPath}.png",
            filteredDetectedText,
            regions,
            verbose=args.verbose,
        )
    else:
        im = None

    # Show image
    if args.display_images:
        image.show(im)

    # Save
    if args.output_dir is not None:
        outputPath = os.path.join(args.output_dir, inputPath)
        if im is not None:
            image.save(im, f"{outputPath}_all.png")
        csvWriter.write(data, f"{outputPath}.csv")

    # Print data
    if args.verbose:
        print("\nExtracted data:")
        for d in data:
            print(f"{list(d.keys())[0]}: {list(d.values())[0]}")
