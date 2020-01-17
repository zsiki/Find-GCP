#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
    GCP finder in a serie of images using opencv aruco markers
    (c) Zoltan Siki siki (dot) zoltan (at) epito.bme.hu
    This code based on
    https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/aruco_basics.html

    Parameters:
        -d, --dict aruco dictionary id (int), default 1 (4X4)
        -o, --output name of output text file, default stdout
        -t, --type target program (ODM, VisualSfM), default ODM
        -i, --input name of input GCP coordinate list file, default None
        -s, --separator separator character in input file, default space
        -v, --verbose verbose output to stdout
        names of input image files
"""
import sys
import os
import argparse
import numpy as np
import cv2
from cv2 import aruco

# set defaults
def_dict = aruco.DICT_4X4_100   # default dictionary 4X4
def_output = sys.stdout         # default output to stdout
def_input = None                # default no input coordinates
def_separator = " "             # default separator is space
def_type = "ODM"                # default output type
# set up command line argument parser
parser = argparse.ArgumentParser()
parser.add_argument('names', metavar='file_names', type=str, nargs='*',
    help='image files to process')
parser.add_argument('-d', '--dict', type=int,
    help='marker dictionary id, default={} (DICT_4X4_100)'.format(def_dict))
parser.add_argument('-o', '--output', type=str,
    help='name of output GCP list file, default stdout')
parser.add_argument('-t', '--type', choices=['ODM', 'VisualSfM'],
    help='target program ODM or VisualSfM, default ODM')
parser.add_argument('-i', '--input', type=str,
    help='name of input GCP coordinate file, default None')
parser.add_argument('-s', '--separator', type=str,
    help='input file separator, default space')
parser.add_argument('-v', '--verbose', action="store_true",
    help='verbose output to stdout')
parser.add_argument('-l', '--list', action="store_true",
    help='output dictionary names and ids and exit')
# parse command line arguments
args = parser.parse_args()
if args.list:
    # list available aruco dictionary names & exit
    for name in aruco.__dict__:
        if name.startswith('DICT_'):
            print('{} : {}'.format(aruco.__dict__[name], name))
    exit(0)
if not args.names:
    print("no input images given")
    parser.print_help()
    exit(0)
# overwrite defaults if param given in command line
if args.dict:
    def_dict = args.dict
if args.output:
    try:
        def_output = open(args.output, 'w')
    except:
        print('cannot open output file')
        exit(1)
if args.type:
    def_type = args.type
if args.input:
    try:
        def_input = open(args.input, 'r')
    except:
        print('cannot open input file')
        exit(2)
if args.separator:
    def_separator = args.separator[0]

# prepare aruco
aruco_dict = aruco.Dictionary_get(def_dict)
parameters = aruco.DetectorParameters_create()
# set some parameters
parameters.minMarkerPerimeterRate = 0.005
parameters.detectInvertedMarker = True
# initialize gcp to image dictionary
gcp_found = {}
# load coordinates from input file
coords = {}
if def_input:
    if args.verbose:
        print("Loading GCP coordinates from {}".format(args.input))
    for line in def_input:
        co = line.strip().split(def_separator)
        if len(co) < 4:
            print("Illegal input: {}".format(line))
            continue
        coords[int(co[0])] = [float(x) for x in co[1:4]]
    def_input.close()
# process image files from command line
for fn in args.names:
    # read actual image file
    if args.verbose:
        print("processing {}".format(fn))
    frame = cv2.imread(fn)
    if frame is None:
        print('error reading image: {}'.format(fn))
        continue
    # convert image to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # find markers
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict,
        parameters=parameters)
    if ids is None:
        print('No markers found on image {}'.format(fn))
        continue
    # check duplicate ids
    idsl = [pid[0] for pid in ids]
    if len(ids) - len(set(idsl)):
        print('duplicate markers on image {}'.format(fn))
        print('marker ids: {}'.format(sorted(ids)))
        continue
    # calculate center & output found markers
    if args.verbose:
        print('  {} GCP markers found'.format(ids.size))
    for i in range(ids.size):
        j = idsl[i]
        if j not in gcp_found:
            gcp_found[j] = []
        gcp_found[j].append(fn)
        # calculate center of aruco code
        x = int(round(np.average(corners[i][0][:,0])))
        y = int(round(np.average(corners[i][0][:,1])))
        if j in coords:
            if def_type == 'ODM':
                def_output.write('{:.3f} {:.3f} {:.3f} {} {} {}\n'.format(
                    coords[j][0], coords[j][1], coords[j][2], x, y,
                    os.path.basename(fn)))
            elif def_type == 'VisualSfM':
                def_output.write('{} {} {} {:.3f} {:.3f} {:.3f}\n'.format(
                    os.path.basename(fn), x, y, coords[j][0], coords[j][1], 
                    coords[j][2]))
        else:
            def_output.write('{} {} {} {}\n'.format(j, x, y,
                os.path.basename(fn)))
if args.verbose:
    for j in gcp_found:
        print('GCP{}: on {} images {}'.format(j, len(gcp_found[j]), gcp_found[j]))
def_output.close()
