from io import BytesIO
from os.path import abspath

files = {}


def add_from_path(name, path):
    with open(abspath(path), "rb") as font_file:
        files[name] = font_file.read()


def get(name):
    return BytesIO(files[name])
