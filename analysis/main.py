import argparse

from commands.compare import compare
from commands.gen_struct_out import gen_struct_out
from commands.visualize_ocr import visualize_ocr
from reader_scripts.list_of_readers import names as format_names


def main():
    args = get_args()

    if args.command == "visualize-ocr":
        visualize_ocr(args)
    elif args.command == "gen-struct-out":
        gen_struct_out(args)
    elif args.command == "compare":
        compare(args)


def get_args():
    parser = argparse.ArgumentParser()

    # Create subparsers for each command
    command_parsers = parser.add_subparsers(
        dest="command", help="command to run"
    )
    command_parsers.required = True

    define_viz_subparser(command_parsers)
    define_gen_subparser(command_parsers)
    define_compare_subparser(command_parsers)

    args = parser.parse_args()
    return args


def define_viz_subparser(command_parsers):
    viz_parser = command_parsers.add_parser(
        "visualize-ocr", help="visualize OCR data"
    )

    viz_parser.description = """Generate images with detected text overlaid on
    the original pictures. Original OCR data consists of pairs of .json and
    .png files."""

    add_ocr_processing_shared_args(viz_parser)


def define_gen_subparser(command_parsers):
    gen_parser = command_parsers.add_parser(
        "gen-struct-out", help="generate structured output from OCR data"
    )

    gen_parser.description = """Generate .csv files of strucured output and
    images with detected text overlaid on the original pictures. Original OCR
    data consists of pairs of .json and .png files."""

    gen_parser.add_argument(
        "-f",
        "--software",
        choices=format_names,
        help="""software on which OCR was performed. If not specified, the
        best matching software is automatically detected.""",
    )

    gen_parser.add_argument(
        "-i",
        "--generate-images",
        action="store_true",
        help="""generate images (takes longer)""",
    )

    add_ocr_processing_shared_args(gen_parser)


def add_ocr_processing_shared_args(parser):
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


def define_compare_subparser(command_parsers):
    compare_parser = command_parsers.add_parser(
        "compare", help="compare structured output with reference"
    )

    compare_parser.description = """Compare two tables (.csv, .xls, or .xlsx)
        of structured output."""

    compare_parser.add_argument("reference", help="""path to reference file""")

    compare_parser.add_argument(
        "file",
        help="""path to file to compare, e.g. output of gen-struct-out""",
    )

    compare_parser.add_argument("-q", "--quiet", action="store_true")


if __name__ == "__main__":
    main()
