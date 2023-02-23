import argparse

from commands.compare import compare
from commands.generateStructuredOutput import generateStructuredOutput
from commands.visualizeOcr import visualizeOcr
from readerScripts.listOfReaders import names as formatNames


def main():
    args = getArgs()

    if args.command == "visualize-ocr":
        visualizeOcr(args)
    elif args.command == "gen-struct-out":
        generateStructuredOutput(args)
    elif args.command == "compare":
        compare(args)


def getArgs():
    parser = argparse.ArgumentParser()

    # Create subparsers for each command
    commandParsers = parser.add_subparsers(
        dest="command", help="command to run"
    )
    commandParsers.required = True

    defineVizSubparser(commandParsers)
    defineGenSubparser(commandParsers)
    defineCompareSubparser(commandParsers)

    args = parser.parse_args()
    return args


def defineVizSubparser(commandParsers):
    vizParser = commandParsers.add_parser(
        "visualize-ocr", help="visualize OCR data"
    )

    vizParser.description = """Generate images with detected text overlaid on
    the original pictures. Original OCR data consists of pairs of .json and
    .png files."""

    addVizGenSharedArgs(vizParser)


def defineGenSubparser(commandParsers):
    genParser = commandParsers.add_parser(
        "gen-struct-out", help="generate structured output from OCR data"
    )

    genParser.description = """Generate .csv files of strucured output and
    images with detected text overlaid on the original pictures. Original OCR
    data consists of pairs of .json and .png files."""

    genParser.add_argument(
        "-f",
        "--software",
        choices=formatNames,
        help="""software on which OCR was performed. If not specified, the
        best matching software is automatically detected.""",
    )

    genParser.add_argument(
        "-i",
        "--generate-images",
        action="store_true",
        help="""generate images (takes longer)""",
    )

    addVizGenSharedArgs(genParser)


def addVizGenSharedArgs(parser):
    parser.add_argument(
        "path",
        help="""path to json file or directory. If path is a directory, all the
        json files in the directory tree are processed.""",
    )

    parser.add_argument(
        "-d",
        "--display-images",
        action="store_true",
        help="""display generated images""",
    )

    parser.add_argument(
        "-o",
        "--output-dir",
        help="""output directory. The tree structure of "path" is replicated
        inside the output directory. To output generated files at the same
        location as input files, use ".".""",
    )

    parser.add_argument("-v", "--verbose", action="store_true")


def defineCompareSubparser(commandParsers):
    compareParser = commandParsers.add_parser(
        "compare", help="compare structured output with reference"
    )

    compareParser.description = """Compare two tables (.csv, .xls, or .xlsx) of
        structured output."""

    compareParser.add_argument("reference", help="""path to reference file""")

    compareParser.add_argument(
        "file",
        help="""path to file to compare, e.g. output of gen-struct-out""",
    )

    compareParser.add_argument("-q", "--quiet", action="store_true")


if __name__ == "__main__":
    main()
