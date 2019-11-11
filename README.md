Licensed under MIT license:
@copyright       (C) xtrose Media Studio 2019
@author          Moses Rivera
                 Im Wiesengrund 24
                 73540 Heubach
@mail            media.studio@xtrose.de

Description:
Recursively compress all .jpg and .png images via tinyPNG API.
All files in the folder and subfolders are processed.
tinypng.py writes and tag to the image metadata (EXIF) so that it is compressed only once.

TinyPNG API Key is needed (500 Pictures free per month:
https://tinypng.com/

WARNING:
Original image is overwritten. Existing metadata (EXIF) will be lost.

Run script:
$ python tinypng "PATH" "APIKEY"