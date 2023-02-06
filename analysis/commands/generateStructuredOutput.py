import os

from models import DetectedText
from readerScripts.findBestReader import findBestReader
from readerScripts.listOfReaders import readers
from utils import csvWriter
from utils import imageManagement as imgm
from utils.getListOfJsonPaths import getListOfJsonPaths


def generateStructuredOutput(args):
    if not args.display_images and args.output_dir is None:
        print("No output method specified. Use -d or -o.")
        quit()

    if args.software is not None:
        desiredReader = readers[args.software]
    else:
        desiredReader = None

    inputPaths = getListOfJsonPaths(args.path, removeExtension=True)
    print(f"Found {len(inputPaths)} .json files:")
    for filename in inputPaths:
        print(f"{filename}.json")
    print("")

    # Loop through all the .json files
    for inputPath in inputPaths:
        processFile(inputPath, args, desiredReader)


def processFile(inputPath, args, desiredReader):
    print(f"Processing {inputPath}")

    # Import detected text from OCR output
    allDetectedText = DetectedText.genListFromFile(f"{inputPath}.json")

    # Define used reader
    if desiredReader is not None:
        reader = desiredReader
    else:
        # Find best reader for this file
        reader = findBestReader(allDetectedText)
        if reader is None:
            print(f"Could not find a matching reader for {inputPath}")
            return

    # Generate structured output
    data, filteredDetectedText, regions = reader.read(allDetectedText)

    # Generate image with detected text
    if args.generate_images or args.display_images:
        im = imgm.generateFromOcrData(
            f"{inputPath}.png",
            filteredDetectedText,
            regions,
            verbose=args.verbose,
        )
    else:
        im = None

    # Show image
    if args.display_images:
        imgm.show(im)

    # Save
    print("TATA", args.output_dir, inputPath)
    if args.output_dir is not None:
        outputPath = os.path.join(args.output_dir, inputPath)
        if im is not None:
            imgm.save(im, f"{outputPath}_filtered.png")
        csvWriter.write(data, f"{outputPath}.csv")

    # Print data
    if args.verbose:
        print("\nExtracted data:")
        for d in data:
            print(f"{list(d.keys())[0]}: {list(d.values())[0]}")
