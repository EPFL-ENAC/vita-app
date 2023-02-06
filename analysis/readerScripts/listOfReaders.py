"""Load Readers from .json configuration files and provide lists of Readers"""

import json

from models.Reader import Reader
from readerScripts import patterns
from utils.getListOfJsonPaths import getListOfJsonPaths


def loadReaders():
    paths = getListOfJsonPaths("readers")
    readers = {}

    for path in paths:
        with open(path) as f:
            readerConf = replacePatterns(json.load(f))
            reader = Reader(readerConf)
            readers[reader.name] = reader

    return readers


def replacePatterns(conf):
    # Replace name and distinctivePattern
    for key, value in conf.items():
        if isinstance(value, str):
            conf[key] = conf[key].format(patterns=patterns)

    # Replace patterns in fields
    for fieldConf in conf["fields"]:
        for key, value in fieldConf.items():
            if isinstance(value, str):
                fieldConf[key] = fieldConf[key].format(patterns=patterns)

    return conf


readers = loadReaders()
names = list(readers.keys())
