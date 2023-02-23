import sys

import Levenshtein
import pandas as pd

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
totalError = 0
nChars = 0
wrongFields = 0
nFields = 0

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
    else:
        try:
            read = float(str(read).replace(",", "."))
        except ValueError:
            pass

    # Save stats
    addedChars = len(str(target))
    nChars += addedChars
    if (not pd.isna(target)) and addedChars > 0:
        nFields += 1

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
        error = Levenshtein.distance(target, read)
        totalError += error
        wrongFields += 1
        print(f"{col}: {read} (expected '{target}', {error} errors)")


print(f"\nTotal error / number of characters: {totalError} / {nChars}")
print(f"Wrong fields: {wrongFields} / {nFields} \n")
