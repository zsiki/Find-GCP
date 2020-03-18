#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import PIL.Image
import PIL.ExifTags
import sys

def to_degrees(dir, value):
    """
    convert the GPS coordinates stored in the EXIF to degress in float format
    :param value: tuples of DMS
    :param dir: direction E/N/W/S
    :returns: decimal degree
    """
    d = float(value[0][0]) / float(value[0][1])
    m = float(value[1][0]) / float(value[1][1])
    s = float(value[2][0]) / float(value[2][1])
    w = 1 if dir in ('E', 'N') else -1
    return w * (d + (m / 60.0) + (s / 3600.0))

def to_num(value):
    """
    convert elevation stored in the EXIF to metric data
    :param value: tuple (int, int)
    :returns: float value
    """
    return(value[0] / value[1])

def img_pos(name):
    """
    get GPS position from image
    :param name: image path
    :returns: tuple of (lat, lon)
    """ 
    img = PIL.Image.open(name)
    exif = img._getexif()
    exif_data = {}
    if exif:
        exif_data = {
            PIL.ExifTags.TAGS[k]: v for k, v in exif.items()
                if k in PIL.ExifTags.TAGS }
    if 'GPSInfo' not in exif_data:
        return None
    return (to_degrees(exif_data['GPSInfo'][3], exif_data['GPSInfo'][4]),
            to_degrees(exif_data['GPSInfo'][1], exif_data['GPSInfo'][2]),
            to_num(exif_data['GPSInfo'][6]))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} image_file(s)".format(sys.argv[0]))
        exit(-1)
    # process parameters
    for name in sys.argv[1:]:
        p = img_pos(name)
        if p:
            print("{},{:.6f},{:.6f},{:.2f}".format(name, p[0], p[1], p[2]))
        else:
            print("{}, NULL, NULL, NULL".format(name))
