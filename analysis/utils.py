import os


def getListOfJsonFilenames(path):
    filenames = []

    # If the path is a file, return a list with the path
    if os.path.isfile(path):
        if path.endswith(".json"):
            filenames.append(path)

    # If the path is a directory, return a list of all the json files in the
    # directory tree
    elif os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for name in files:
                if name.endswith(".json"):
                    filenames.append(os.path.join(root, name))

    if len(filenames) == 0:
        print("No json files found in the specified path.")
        quit()

    print(f"Found {len(filenames)} json files:")
    for filename in filenames:
        print(filename)

    return filenames
