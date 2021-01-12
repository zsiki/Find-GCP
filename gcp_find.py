#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    GCP finder in a serie of images using opencv aruco markers
    (c) Zoltan Siki siki (dot) zoltan (at) epito.bme.hu
    This code based on
    https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/aruco_basics.html
    for details see:
    https://docs.opencv.org/trunk/d5/dae/tutorial_aruco_detection.html

    for usage help:
    gcp_find.py --help
"""
import sys
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import cv2

aruco = cv2.aruco
params = aruco.DetectorParameters_create()
# set defaults
def_dict = aruco.DICT_4X4_100   # default dictionary 4X4
def_output = sys.stdout         # default output to stdout
def_input = None                # default no input coordinates
def_separator = " "             # default separator is space
def_type = ""                # default output type
# set up command line argument parser
parser = argparse.ArgumentParser()
parser.add_argument('names', metavar='file_names', type=str, nargs='*',
    help='image files to process')
parser.add_argument('-d', '--dict', type=int, default=def_dict,
    help='marker dictionary id, default={} (DICT_4X4_100)'.format(def_dict))
parser.add_argument('-o', '--output', type=str, default=def_output,
    help='name of output GCP list file, default stdout')
parser.add_argument('-t', '--type', choices=['ODM', 'VisualSfM'],
    default=def_type,
    help='target program ODM or VisualSfM, default {}'.format(def_type))
parser.add_argument('-i', '--input', type=str, default=def_input,
    help='name of input GCP coordinate file, default {}'.format(def_input))
parser.add_argument('-s', '--separator', type=str, default=' ',
    help='input file separator, default {}'.format(def_separator))
parser.add_argument('-v', '--verbose', action="store_true",
    help='verbose output to stdout')
parser.add_argument('-r', '--inverted', action="store_true",
    help='detect inverted markers')
parser.add_argument('--debug', action="store_true",
    help='show detected markers on image')
parser.add_argument('--winmin', type=int, default=params.adaptiveThreshWinSizeMin,
    help='adaptive tresholding window min size, default {}'.format(params.adaptiveThreshWinSizeMin))
parser.add_argument('--winmax', type=int, default=params.adaptiveThreshWinSizeMax,
    help='adaptive thresholding window max size, default {}'.format(params.adaptiveThreshWinSizeMax))
parser.add_argument('--winstep', type=int, default=params.adaptiveThreshWinSizeStep,
    help='adaptive thresholding window size step , default {}'.format(params.adaptiveThreshWinSizeStep))
parser.add_argument('--thres', type=float, default=params.adaptiveThreshConstant,
    help='adaptive threshold constant, default {}'.format(params.adaptiveThreshConstant))
parser.add_argument('--minrate', type=float, default=params.minMarkerPerimeterRate,
    help='min marker perimeter rate, default {}'.format(params.minMarkerPerimeterRate))
parser.add_argument('--maxrate', type=float, default=params.maxMarkerPerimeterRate,
    help='max marker perimeter rate, default {}'.format(params.maxMarkerPerimeterRate))
parser.add_argument('--poly', type=float, default=params.polygonalApproxAccuracyRate,
    help='polygonal approx accuracy rate, default {}'.format(params.polygonalApproxAccuracyRate))
parser.add_argument('--corner', type=float, default=params.minCornerDistanceRate,
    help='minimum distance any pair of corners in the same marker, default {}'.format(params.minCornerDistanceRate))
parser.add_argument('--markerdist', type=float, default=params.minMarkerDistanceRate,
    help='minimum distance any pair of corners from different markers, default {}'.format(params.minMarkerDistanceRate))
parser.add_argument('--borderdist', type=int, default=params.minDistanceToBorder,
    help='minimum distance any marker corner to image border, default {}'.format(params.minDistanceToBorder))
parser.add_argument('--borderbits', type=int, default=params.markerBorderBits,
    help='width of marker border, default {}'.format(params.markerBorderBits))
parser.add_argument('--otsu', type=float, default=params.minOtsuStdDev,
    help='minimum stddev of pixel values, default {}'.format(params.minOtsuStdDev))
parser.add_argument('--persp', type=int, default=params.perspectiveRemovePixelPerCell,
    help='number of pixels per cells, default {}'.format(params.perspectiveRemovePixelPerCell))
parser.add_argument('--ignore', type=float, default=params.perspectiveRemoveIgnoredMarginPerCell,
    help='Ignored pixels at cell borders, default {}'.format(params.perspectiveRemoveIgnoredMarginPerCell))
parser.add_argument('--error', type=float, default=params.maxErroneousBitsInBorderRate,
    help='Border bits error rate, default {}'.format(params.maxErroneousBitsInBorderRate))
parser.add_argument('--correct', type=float, default=params.errorCorrectionRate,
    help='Bit correction rate, default {}'.format(params.errorCorrectionRate))
parser.add_argument('--refinement', type=int, default=params.cornerRefinementMethod,
    help='Subpixel process method, default {}'.format(params.cornerRefinementMethod))
parser.add_argument('--refwin', type=int, default=params.cornerRefinementWinSize,
    help='Window size for subpixel refinement, default {}'.format(params.cornerRefinementWinSize))
parser.add_argument('--maxiter', type=int, default=params.cornerRefinementMaxIterations,
    help='Stop criteria for subpixel process, default {}'.format(params.cornerRefinementMaxIterations))
parser.add_argument('--minacc', type=float, default=params.cornerRefinementMinAccuracy,
    help='Stop criteria for subpixel process, default {}'.format(params.cornerRefinementMinAccuracy))
parser.add_argument('-l', '--list', action="store_true",
    help='output dictionary names and ids and exit')
# parse command line arguments
args = parser.parse_args()
if args.list:
    # list available aruco dictionary names & exit
    wl = [(99, 'DICT_3X3_32 custom')]
    for name in aruco.__dict__:
        if name.startswith('DICT_'):
            wl.append((aruco.__dict__[name], name))
    for w in sorted(wl):
        print('{} : {}'.format(w[0], w[1]))
    sys.exit(0)
if not args.names:
    print("no input images given")
    parser.print_help()
    sys.exit(0)
if args.output == sys.stdout:
    foutput = args.output
else:
    try:
        foutput = open(args.output, 'w')
    except:
        print('cannot open output file')
        sys.exit(1)
if args.input:
    try:
        finput = open(args.input, 'r')
    except:
        print('cannot open input file')
        sys.exit(2)

# prepare aruco
if args.dict == 99:     # use special 3x3 dictionary
    aruco_dict = aruco.Dictionary_create(32, 3)
else:
    aruco_dict = aruco.Dictionary_get(args.dict)
    
# set parameters
params.detectInvertedMarker = args.inverted
params.adaptiveThreshWinSizeMin = args.winmin
params.adaptiveThreshWinSizeMax = args.winmax
params.adaptiveThreshWinSizeStep = args.winstep
params.adaptiveThreshConstant = args.thres
params.minMarkerPerimeterRate = args.minrate
params.maxMarkerPerimeterRate = args.maxrate
params.polygonalApproxAccuracyRate = args.poly
params.minCornerDistanceRate = args.corner
params.minMarkerDistanceRate = args.markerdist
params.minDistanceToBorder = args.borderdist
params.markerBorderBits = args.borderbits
params.minOtsuStdDev = args.otsu
params.perspectiveRemovePixelPerCell = args.persp
params.perspectiveRemoveIgnoredMarginPerCell = args.ignore
params.maxErroneousBitsInBorderRate = args.error
params.errorCorrectionRate = args.correct
params.cornerRefinementMethod = args.refinement
params.cornerRefinementWinSize = args.refwin
params.cornerRefinementMaxIterations = args.maxiter
params.cornerRefinementMinAccuracy = args.minacc
# initialize gcp to image dictionary
gcp_found = {}
# load coordinates from input file
coords = {}
if args.input:
    if args.verbose:
        print("Loading GCP coordinates from {}".format(args.input))
    for line in finput:
        co = line.strip().split(args.separator)
        if len(co) < 4:
            print("Illegal input: {}".format(line))
            continue
        coords[int(co[0])] = [float(x) for x in co[1:4]]
    finput.close()
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
        parameters=params)
    #if args.debug and rejectedImgPoints:
    #    print('{} rejected points on {}'.format(len(rejectedImgPoints), fn))
    #    plt.figure()
    #    plt.title("rejected")
    #    plt.imshow(frame)
    #    for i in range(len(rejectedImgPoints)):
    #        x = int(round(np.average(rejectedImgPoints[i][:, 0])))
    #        y = int(round(np.average(rejectedImgPoints[i][:, 1])))
    #        plt.plot(x, y, "o", label="id={}".format(i))
    #    plt.show()
    if ids is None:
        print('No markers found on image {}'.format(fn))
        continue
    # check duplicate ids
    idsl = [pid[0] for pid in ids]
    if len(ids) - len(set(idsl)):
        print('duplicate markers on image {}'.format(fn))
        print('marker ids: {}'.format(sorted(idsl)))
    # calculate center & output found markers
    if args.verbose:
        print('  {} GCP markers found'.format(ids.size))
    if args.debug:  # show found ids in debug mode
        plt.figure()
        plt.title("{} GCP, {} duplicate found on {}".format(len(ids), len(ids) - len(set(idsl)), fn))
        aruco.drawDetectedMarkers(frame, corners, ids)
        plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    for i in range(ids.size):
        j = ids[i][0]
        if j not in gcp_found:
            gcp_found[j] = []
        gcp_found[j].append(fn)
        # calculate center of aruco code
        x = int(round(np.average(corners[i][0][:, 0])))
        y = int(round(np.average(corners[i][0][:, 1])))
        if args.type == 'ODM':
            if j in coords:
                foutput.write('{:.3f} {:.3f} {:.3f} {} {} {}\n'.format(
                    coords[j][0], coords[j][1], coords[j][2], x, y,
                    os.path.basename(fn)))
            else:
                print("No coordinates for {}".format(j))
        elif args.type == 'VisualSfM':
            if j in coords:
                foutput.write('{} {} {} {:.3f} {:.3f} {:.3f}\n'.format(
                    os.path.basename(fn), x, y, coords[j][0], coords[j][1], 
                    coords[j][2]))
            else:
                print("No coordinates for {}".format(j))
        else:
            if j in coords:
                foutput.write('{:.3f} {:.3f} {:.3f} {} {} {}\n'.format(
                    coords[j][0], coords[j][1], coords[j][2], x, y,
                    os.path.basename(fn)))
            else:
                foutput.write('{} {} {} {}\n'.format(j, x, y,
                    os.path.basename(fn)))
        if args.debug:
            if j in coords:
                plt.plot(x, y, "o", label="id={}".format(ids[i]))
            else:
                plt.plot(x, y, "x", label="id={}".format(ids[i]))
    if args.debug:
        #plt.legend()
        plt.show()

if args.verbose:
    for j in gcp_found:
        print('GCP{}: on {} images {}'.format(j, len(gcp_found[j]), gcp_found[j]))
foutput.close()
