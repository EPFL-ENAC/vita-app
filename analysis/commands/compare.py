import Levenshtein
import pandas as pd

date_format = "%d/%m/%Y"


def load_table(path):
    if path.endswith(".csv"):
        return pd.DataFrame(pd.read_csv(path))
    elif path.endswith(".xls") or path.endswith(".xlsx"):
        return pd.read_excel(path)
    else:
        print("File format not supported")
        quit()


def compare(args):
    reference = load_table(args.reference)
    file = load_table(args.file)
    verbose = not args.quiet
    total_error = 0
    total_char_count = 0
    wrong_fields = 0
    field_count = 0

    # Compare each entry
    for col in reference:
        if col not in file:
            if verbose:
                print(f"Column '{col}' not found in file")
            continue

        target = reference[col][0]
        read = file[col][0]
        field_empty, new_char_count, error = compare_entry(
            col, target, read, verbose
        )

        if field_empty:
            continue

        field_count += 1
        if error > 0:
            wrong_fields += 1
            total_error += error

        total_char_count += new_char_count

    if verbose:
        print(
            f"\nTotal error / number of characters: {total_error} /"
            f" {total_char_count}"
        )
        print(f"Wrong fields: {wrong_fields} / {field_count} \n")

    return total_error, total_char_count, wrong_fields, field_count


def compare_entry(col, target, read, verbose=False):
    match col:
        # Reformat last name (full caps in some documents)
        case "Last name":
            target = str(target).title()
            read = str(read).title()

        # Format dates
        case "DOB" | "Date of consultation":
            if type(target) == pd.Timestamp:
                target = target.strftime(date_format)
            if type(read) == pd.Timestamp:
                read = read.strftime(date_format)

        # Format floats that have a comma instead of a dot
        case _:
            try:
                read = float(str(read).replace(",", "."))
            except ValueError:  # Cannot cast to float
                pass

    # Count characters in read field
    new_chars = len(str(target))
    if pd.isna(target) or new_chars == 0:  # Empty field
        return True, 0, 0

    # Maching
    if target == read or (pd.isna(target) and pd.isna(read)):
        if verbose:
            if pd.isna(target):
                print(f"{col}:")
            else:
                print(f"{col}: {target}")
        return False, new_chars, 0

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
        return False, new_chars, error
