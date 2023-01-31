import sys
import pandas as pd
import numpy as np
import Levenshtein


if len(sys.argv) != 3:
    print("\nUsage: python3 compare.py reference file")
    print("'reference' and 'file' can be .csv or .xlsx files")
    quit()

referencePath = sys.argv[1]
filePath = sys.argv[2]


dateFormat = "%d/%m/%Y"


# Load tables
def load(path):
    if path.endswith(".csv"):
        return pd.DataFrame(pd.read_csv(path))
    elif path.endswith(".xlsx"):
        return pd.read_excel(path)
    else:
        print("File format not supported")
        quit()

reference = load(referencePath)
file = load(filePath)
totalDist = 0

# Compare each entry
for col in reference:
    if col not in file:
        print(f"Column '{col}' not found in file")

    target = reference[col][0]
    read = file[col][0]


    # Reformat last name (full caps in documents)
    if col == "Last name":
        target = str(target).title()
        read = str(read).title()

    # Format dates
    elif col == "DOB" or col == "Date of consultation":
        if type(target) == pd.Timestamp:
            target = target.strftime(dateFormat)
        if type(read) == pd.Timestamp:
            read = read.strftime(dateFormat)

    # Format floats that have a comma instead of a dot
    elif isinstance(target, np.floating):
        try:
            read = float(str(read).replace(",", "."))
        except ValueError:
            pass

    # Maching
    if target == read or (pd.isna(target) and pd.isna(read)):
        if pd.isna(target):
            print(f"{col}:")
        else:
            print(f"{col}: {target}")

    # Not matching
    else:
        target = str(target)
        read = str(read)
        if target == "nan":
            target = ""
        if read == "nan":
            read = ""
        dist = Levenshtein.distance(target, read)
        totalDist += dist
        print(f"{col}: {read} (expected '{target}', distance {dist})")


print(f"\nTotal distance: {totalDist}\n")
