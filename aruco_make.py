#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    Simple application to generate ArUco markers of different dictionaries
"""
import argparse
import packaging.version
import cv2
from cv2 import aruco
import matplotlib.pyplot as plt

# handle incompatibility introduced in openCV 4.8
if packaging.version.parse(cv2.__version__) < packaging.version.parse('4.7'):
    aruco.extendDictionary = aruco.Dictionary_create
    aruco.getPredefinedDictionary = aruco.Dictionary_get
    aruco.generateImageMarker = aruco.drawMarker

def_dict = aruco.DICT_4X4_100   # default dictionary 4X4
def_start = 0                   # first marker to generate
def_end = -1                    # last marker to generate
def_gray = 95                   # gray color
def_pad = 0.5                   # border around marker in inches

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
parser.add_argument('-g', '--gray', action="store_true",
    help='generate black/gray marker to reduce burnt in effect')
parser.add_argument('--value', type=int, default=def_gray,
    help='shade of background use with --gray, default= {}'.format(def_gray))
parser.add_argument('-p', '--pad', type=float, default=def_pad,
    help='border width around marker in inches, default= {}'.format(def_pad))
args = parser.parse_args()

if args.dict == 99:     # use special 3x3 dictionary
    aruco_dict = aruco.extendDictionary(32, 3)
else:
    aruco_dict = aruco.getPredefinedDictionary(args.dict)
if args.end < args.start:
    args.end = args.start
for i in range(args.start, args.end+1):
    img = aruco.generateImageMarker(aruco_dict, i, 1000)
    if args.gray:
        img[img == 255] = args.value
        plt.figure(facecolor=str(args.value/255))
    plt.axis('off')
    plt.imshow(img, cmap='gray', vmin=0, vmax=255, interpolation='nearest')
    plt.savefig("marker{}.png".format(i), bbox_inches='tight', pad_inches=args.pad)
    if args.view:
        plt.show()
