import os


def getListOfJsonPaths(pathIni):
    paths = []

    # If the path is a file, put only this file in the list
    if os.path.isfile(pathIni):
        if pathIni.endswith(".json"):
            paths.append(pathIni)

    # If the path is a directory, create a list of all the json files in the
    # directory tree
    elif os.path.isdir(pathIni):
        for root, dirs, files in os.walk(pathIni):
            for name in files:
                if name.endswith(".json"):
                    paths.append(os.path.join(root, name))

    if len(paths) == 0:
        print("No .json files found in the specified path.")
        quit()

    print(f"Found {len(paths)} .json files:")
    for filename in paths:
        print(filename)
    print("")

    # Remove .json extension
    paths = [os.path.splitext(f)[0] for f in paths]

    return paths
