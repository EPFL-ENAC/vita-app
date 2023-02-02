# VITA'App

_Picture to Structured Text_

Read an eye examination medical report using a mobile iOS device and extract the relevant data in a `.csv` file.


# 🖥 Supported document layouts

Alcon EX500, Sophtalmo


# 📱 iOS application (OCR)

## Development and usage

Development can be done in the xCode software running on macOS. To test the application, one must upload it to a real non-simulated device (either iPhone or iPad) to use the camera.

After usage, cropped images and JSON files containing text informations are saved in the application folder on the device. These files can be retrieved on a computer by plugging the device and manually transferring the files.

_Note: The application layout is built using UIKit._


# 🧮 Structured text analysis

The analysis of the OCR text is performed by the script `analysis/structuredOutput.py`.

## Requirements

- Python 3.10
- Make
- [Poetry](https://python-poetry.org/docs/#installation)

## Installation

```
make install
```

## Input files

Retreive the OCR files `xxx.json` and `xxx.png` from the iOS device and put them on your computer. The pairs of `.json` and `.png` files must be in the same directory.

## Visualizing the OCR's output

```
cd analysis
poetry run python3 main.py visualize-ocr path_to.json --display-images --o outputs/
```
Shows the picture overlaid with detected OCR text and saves it in the `outputs` directory, following the same tree structure from as `path_to` (outputs will be in `outputs/path_to...`).

Multiple files can be processed at once:
```
poetry run python3 main.py visualize-ocr path_to_directory/ --o outputs/
```

## Structured output

```
poetry run python3 main.py gen-struct-out path_to.json [-f software] --display-images --o outputs/
```
An image displaying the useful fields is shown and a `.csv` file is written in the `outputs` directory.
Similarly to visualizing OCR output, Multiple files can be processed at once.

If `software` is not specified, the best matching software will be automatically selected. `software` can be either `"Alcon EX500"` or `"Sophtalmo"`.

## Testing installation
```
make test
```

## Short documentation

`command/generateStructuredOutput.py` is the entry point of the analysis. The OCR `.json` file is read to create a list of `DetectedText`, defined in `DetectedText.py`, with information on the read text and the bounding boxes. Then, data is extracted from this list using a specific reader (for example, look at a definition in `readers/alconEx500.py`). The reader rely on fuzzy string matching and relative positioning of bounding boxes (see `readers/search.py`).

