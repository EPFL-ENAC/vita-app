import csv
import os


def write(data, path):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)

    f = open(path, "w")
    writer = csv.writer(f)
    writer.writerow([list(entry.keys())[0] for entry in data])
    writer.writerow([list(entry.values())[0] for entry in data])
    f.close()
