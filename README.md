# VITA'App

_Picture to Structured Text_

Read an eye examination medical report using a mobile iOS device and extract the relevant data in a `.csv` file.


# Supported document layouts

Alcon EX500, Sophtalmo


# iOS application (OCR)

## Development and usage

Development can be done in the xCode software running on macOS. To test the application, one must upload it to a real non-simulated device (either iPhone or iPad) to use the camera.

After usage, cropped images and JSON files containing text informations are saved in the application folder on the device. These files can be retrieved on a computer by plugging the device and manually transferring the files.

_Note: The application layout is built using UIKit._


# Structured text analysis

The analysis of the OCR text is performed by the script `analysis/structuredOutput.py`.

## Installation

_Recommended:_ Setup a virtual Python environment:
```
python3 -m venv env
source env/bin/activate
```
Install required packages:
```
pip install -r requirements.txt
```

## Input files

Put the OCR files `xxx.json` and `xxx.png` in `analysis/inputs`.

## Visualizing the OCR's output

```
cd analysis
python3 visualizeOcr.py inputs/xxx.json
```

## Running

```
python3 structuredOutput.py inputs/xxx.json
```

An image displaying the found fields is shown and a `.csv` file is written in the `analysis/outputs` directory.

## Testing installation
Run the following command from the `analysis` diretory:
```
pytest
```

## Short documentation

`structuredOutput.py` is the entry point of the analysis. The OCR `.json` file is read to create a list of `DetectedText`, defined in `DetectedText.py`, with information on the read text and the bounding boxes. Then, data is extracted from this list using a specific reader (for example, look at a definition in `readers/alconEx500.py`). The reader rely on fuzzy string matching and relative positioning of bounding boxes (see `readers/search.py`).

