#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
    Generate coordinate list from exif info of images
    (C) Zoltan Siki
"""
# TODO use exiftool instead of PIL to get yaw, pitch, roll and other metadata

import sys
import PIL.Image
import PIL.ExifTags

def to_degrees(direction, value):
    """
    convert the GPS coordinates stored in the EXIF to degress in float format
    :param value: tuples of DMS
    :param dir: direction E/N/W/S
    :returns: decimal degree
    """
    try:
        angle_deg = float(value[0][0]) / float(value[0][1])
        angle_min = float(value[1][0]) / float(value[1][1])
        angle_sec = float(value[2][0]) / float(value[2][1])
    except:
        angle_deg, angle_min, angle_sec = value
    angle_dir = 1 if direction in ('E', 'N') else -1
    return angle_dir * (angle_deg + (angle_min / 60.0) + (angle_sec / 3600.0))

def to_num(value):
    """
    convert elevation stored in the EXIF to metric data
    :param value: tuple (int, int)
    :returns: float value
    """
    try:
        ret = value[0] / value[1]
    except:
        ret = float(value)
    return ret

def img_pos(name):
    """
    get GPS position from image
    :param name: image path
    :returns: tuple of (lat, lon)
    """
    with PIL.Image.open(name) as img:
        try:
            exif = img._getexif()
        except AttributeError:
            exif = None
    ret = []
    if exif is not None:
        exif_data = {PIL.ExifTags.TAGS[k]: v for k, v in exif.items()
                     if k in PIL.ExifTags.TAGS}
        if 'GPSInfo' in exif_data and len(exif_data['GPSInfo']) > 6:
            ret = [to_degrees(exif_data['GPSInfo'][3], exif_data['GPSInfo'][4]),
                   to_degrees(exif_data['GPSInfo'][1], exif_data['GPSInfo'][2]),
                   to_num(exif_data['GPSInfo'][6])]
        if 'DateTime' in exif_data:
            ret.append(exif_data['DateTime'])
    return ret

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} image_file(s)".format(sys.argv[0]))
        sys.exit(1)
    # process parameters
    for iname in sys.argv[1:]:
        p = img_pos(iname)
        if len(p) > 3:          # position and datetime found?
            print("{},{:.6f},{:.6f},{:.2f},{}".format(iname, p[0], p[1], p[2], p[3]))
        elif len(p) == 3:       # position found?
            print("{},{:.6f},{:.6f},{:.2f}".format(iname, p[0], p[1], p[2]))
        elif len(p) == 1:       # datetiem found?
            print("{},,,,{}".format(iname, p[0]))
        else:
            print("{},,,,,No EXIF".format(iname))
