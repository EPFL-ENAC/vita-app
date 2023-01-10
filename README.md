# VITA'App

_Picture to Structured Text_


# iOS application

## Development and usage

Development can be done in the xCode software running on macOS. To test the application, one must upload it to a real non-simulated device (either iPhone or iPad) to use the camera.

After usage, a cropped image and a JSON file are saved in the application folder on the device.

_Note: The application layout is built using UIKit._


# Structured text analysis

The analysis of the OCR text is performed by the script `analysis/structuredOutput.py`.

## Installation

```
pip install -r requirements.txt
```

## Input files

Put `detectedText.json` and `cropped.png` in `analysis/inputs`.

## Running

```
cd analysis
python3 structuredOutput.py
```


# Supported document layouts

_To be added_

