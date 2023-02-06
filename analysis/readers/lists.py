from readers import alconEx500, sophtalmo

formats = [alconEx500, sophtalmo]
names = [f.reader.name for f in formats]

readers = {}
for f in formats:
    readers[f.reader.name] = f.reader
