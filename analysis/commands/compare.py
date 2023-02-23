import Levenshtein
import pandas as pd

dateFormat = "%d/%m/%Y"


def loadTable(path):
    if path.endswith(".csv"):
        return pd.DataFrame(pd.read_csv(path))
    elif path.endswith(".xls") or path.endswith(".xlsx"):
        return pd.read_excel(path)
    else:
        print("File format not supported")
        quit()


def compare(args):
    reference = loadTable(args.reference)
    file = loadTable(args.file)
    verbose = not args.quiet
    totalError = 0
    totalCharCount = 0
    wrongFields = 0
    fieldCount = 0

    # Compare each entry
    for col in reference:
        if col not in file:
            if verbose:
                print(f"Column '{col}' not found in file")
            continue

        target = reference[col][0]
        read = file[col][0]
        fieldEmpty, newCharCount, error = compareEntry(
            col, target, read, verbose
        )

        if fieldEmpty:
            continue

        fieldCount += 1
        if error > 0:
            wrongFields += 1
            totalError += error

        totalCharCount += newCharCount

    if verbose:
        print(
            f"\nTotal error / number of characters: {totalError} /"
            f" {totalCharCount}"
        )
        print(f"Wrong fields: {wrongFields} / {fieldCount} \n")

    return totalError, totalCharCount, wrongFields, fieldCount


def compareEntry(col, target, read, verbose=False):
    # Reformat last name (full caps in some documents)
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

    # Count characters in read field
    newChars = len(str(target))
    if pd.isna(target) or newChars == 0:  # Empty field
        return True, 0, 0

    # Maching
    if target == read or (pd.isna(target) and pd.isna(read)):
        if verbose:
            if pd.isna(target):
                print(f"{col}:")
            else:
                print(f"{col}: {target}")
        return False, newChars, 0

    # Not matching
    else:
        target = str(target)
        read = str(read)
        if target == "nan":
            target = ""
        if read == "nan":
            read = ""
        error = Levenshtein.distance(target, read)
        if verbose:
            print(f"{col}: {read} (expected '{target}', {error} errors)")
        return False, newChars, error
