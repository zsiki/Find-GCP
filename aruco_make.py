#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    Simple application to generate ArUco markers of different dictionaries
"""
import argparse
from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl

def_dict = aruco.DICT_4X4_100   # default dictionary 4X4
def_start = 0                   # first marker to generate
def_end = -1                    # last marker to generate
def_grey = 95                   # grey color

# set up command line argument parser
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dict', type=int, default=def_dict,
    help='marker dictionary id (use 99 for 3x3 markers), default= {} (DICT_4X4_100)'.format(def_dict))
parser.add_argument('-s', '--start', type=int, default=def_start,
    help='first marker to generate, default= {}'.format(def_start))
parser.add_argument('-e', '--end', type=int, default=def_end,
    help='last marker to generate default= {}'.format(def_end))
parser.add_argument('-v', '--view', action="store_true",
    help='show marker on monitor')
parser.add_argument('-g', '--grey', action="store_true",
    help='generate black/grey marker to reduce burnt in effect')
args = parser.parse_args()

if args.dict == 99:     # use special 3x3 dictionary
    aruco_dict = aruco.Dictionary_create(32, 3)
else:
    aruco_dict = aruco.Dictionary_get(args.dict)
if args.end < args.start:
    args.end = args.start
#fig = plt.figure()
for i in range(args.start, args.end+1):
    img = aruco.drawMarker(aruco_dict, i, 1000)
    if args.grey:
        img[img[:,:] == 255] = def_grey
        plt.figure(facecolor=str(def_grey/255))
    plt.axis('off')
    plt.imshow(img, cmap=mpl.cm.gray, vmin=0, vmax=255, interpolation="nearest")
    plt.savefig("marker{}.png".format(i), bbox_inches='tight', pad_inches=0.5)
    if args.view:
        plt.show()
