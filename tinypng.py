#!/usr/bin/python3.6

# Imports.
import sys
import os
import tinify
import piexif
from PIL import Image
from PIL.ExifTags import TAGS


# Variables.
apiKey = ''  # https://tinypng.com API Key


# Welcome message-
def welcomeMessage():
    print('\nWelcome to xtrose Media Studios tinypng.py\nhttps://www.xtrose.com\n')
    init()


# Initialize
def init():
    global apiKey

    if len(sys.argv) < 2:
        exit('Error: No path as argument passed.\nTry: $ python tinypng.py "PATH" "APIKEY"\n')
    path = sys.argv[1]

    if apiKey == '':
        if len(sys.argv) < 3:
            exit('Error: TinyPNG API Key not defined and not as argument passed.\nWrite TinyPNG API Key in file or Try: $ python tinypng.py "PATH" "APIKEY"\n')
        apiKey = sys.argv[2]

    if not os.path.isdir(path):
        exit('Error: Path not exists.')

    getImages(path)


def getImages(path):
    jpgComplete = 0
    jpgTinified = 0
    pngComplete = 0
    pngTinified = 0

    for root, subdirs, files in os.walk(path):
        for file in files:
            name, extension = os.path.splitext(file)
            if extension == '.jpg':
                jpgComplete += 1
                tinified = tinifyImage(os.path.join(root, file), 'jpeg')
                if tinified:
                    jpgTinified +=1
            elif extension == '.png':
                pngComplete += 1
                tinified = tinifyImage(os.path.join(root, file), 'png')
                if tinified:
                    pngTinified += 1

    print('Job done')
    print(jpgTinified, 'of', jpgComplete, 'jpg images tinified.')
    print(pngTinified, 'of', pngComplete, 'png images tinified.\n')
    exit()


# Tinify image.
def tinifyImage(path, extension):
    allreadyTinified = getIfTinified(path)
    if allreadyTinified:
        return False

    print('Tinify:', path)
    sizeBefore = os.path.getsize(path)

    array = path.split('/')
    array[len(array) - 1] = '__' + array[len(array) - 1]
    tinifiedPath = '/'.join(array)
    tinify.key = apiKey
    source = tinify.from_file(path)
    source.to_file(tinifiedPath)

    if not os.path.isfile(tinifiedPath):
        return False

    setExif(tinifiedPath, extension)
    os.remove(path)
    os.rename(tinifiedPath, path)

    sizeAfter = os.path.getsize(path)
    reduce = 100 - (100.0 / sizeBefore * sizeAfter)
    reduce = round(reduce)
    print('Tinified:', reduce, '%\n')

    return True


# Get if image tinified.
def getIfTinified(path):
    meta = {}
    image = Image.open(path)
    info = image.getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        meta[decoded] = value
    if 'Artist' in meta:
        if meta['Artist'] == 'tinypng':
            return True
    return False


# Set image metadata (EXIF).
def setExif(path, extension):
    zeroth_ifd = {
        piexif.ImageIFD.Artist: 'tinypng'
    }
    exif_dict = {"0th": zeroth_ifd}
    exif_bytes = piexif.dump(exif_dict)
    with open(path, 'r+b') as f:
        with Image.open(path, 'r') as image:
            image.save(path, extension, exif=exif_bytes)


# Welcome message
welcomeMessage()
