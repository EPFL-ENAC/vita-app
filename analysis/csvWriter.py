import csv


def write(data, path):
    f = open(path, "w")
    writer = csv.writer(f)
    writer.writerow([list(entry.keys())[0] for entry in data])
    writer.writerow([list(entry.values())[0] for entry in data])
    f.close()
