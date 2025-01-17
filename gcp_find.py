#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    GCP finder in a serie of images using opencv aruco markers
    (c) Zoltan Siki siki (dot) zoltan (at) emk.bme.hu
    This code based on
    https://mecaruco2.readthedocs.io/en/latest/notebooks_rst/Aruco/aruco_basics.html
    for details see:
    https://docs.opencv.org/trunk/d5/dae/tutorial_aruco_detection.html

    for usage help:
    gcp_find.py --help
"""
import sys
import os
import time
import glob
import json
import argparse
import packaging.version
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import cv2
from cv2 import aruco
from process_raw import DngFile

# handle incompatibility introduced in openCV 4.8
if packaging.version.parse(cv2.__version__) < packaging.version.parse('4.8'):
    aruco.extendDictionary = aruco.Dictionary_create
    aruco.getPredefinedDictionary = aruco.Dictionary_get
    aruco.DetectorParameters = aruco.DetectorParameters_create

class GcpFind():
    """ class to collect GCPs on an image """
    LUT_IN = [0, 158, 216, 255]
    LUT_OUT = [0, 22, 80, 176]

    def __init__(self, args, params):
        """ Initialize GcpFind object

            :param args: processed command line parameters
            :param params: aruco find params
        """
        self.args = args
        # prepare aruco
        if args.dict == 99:     # use special 3x3 dictionary
            self.aruco_dict = aruco.extendDictionary(32, 3)
        else:
            self.aruco_dict = aruco.getPredefinedDictionary(args.dict)

        # set aruco parameters from command line arguments
        self.params = params
        if args.aruco_params is None:
            self.params.adaptiveThreshConstant = args.thres
            self.params.adaptiveThreshWinSizeMax = args.winmax
            self.params.adaptiveThreshWinSizeMin = args.winmin
            self.params.adaptiveThreshWinSizeStep = args.winstep
            self.params.cornerRefinementMaxIterations = args.maxiter
            self.params.cornerRefinementMethod = args.refinement
            self.params.cornerRefinementMinAccuracy = args.minacc
            self.params.cornerRefinementWinSize = args.refwin
            self.params.detectInvertedMarker = args.inverted
            self.params.errorCorrectionRate = args.correctionrate
            self.params.markerBorderBits = args.borderbits
            self.params.maxErroneousBitsInBorderRate = args.error
            self.params.maxMarkerPerimeterRate = args.maxrate
            self.params.minCornerDistanceRate = args.corner
            self.params.minDistanceToBorder = args.borderdist
            self.params.minMarkerDistanceRate = args.markerdist
            self.minMarkerLengthRatioOriginalImg = args.lengthratio
            self.params.minMarkerPerimeterRate = args.minrate
            self.params.minOtsuStdDev = args.otsu
            self.params.perspectiveRemoveIgnoredMarginPerCell = args.ignore
            self.params.perspectiveRemovePixelPerCell = args.persp
            self.params.polygonalApproxAccuracyRate = args.poly
            self.params.useAruco3Detection = args.aruco3
        else :
            # read params from json
            with open(args.aruco_params, encoding='ascii') as f:
                data = f.read()
            js = json.loads(data)
            for par in js:
                setattr(self.params, par, js[par])
        if args.list:
            # list available aruco dictionary names & exit
            for act_dict in self.list_dicts():
                print(f'{act_dict[0]} : {act_dict[1]}', file=sys.stderr)
            # list all aruco parameters
            for par in dir(self.params):
                if not par.startswith('__'):
                    val = getattr(self.params, par)
                    if type(val) in (int, float, str, bool):
                        print(f'{par} : {val}', file=sys.stderr)
            sys.exit(0)

        self.coords = {}
        self.gcp_found = {}          # initialize gcp to image dict
        if not self.check_params():
            sys.exit(1)

        if self.args.input:
            # load GCP coords
            self.coo_input()

        # lookup table for color correction
        self.lut = np.interp(np.arange(0, 256), self.LUT_IN,
                             self.LUT_OUT).astype(np.uint8)
        self.gcps = []  # list for found gcps

    @staticmethod
    def list_dicts():
        """ collects available aruco dictionary names

            :return: sorted list of available AruCo dictionaries
        """
        dicts = {99: 'DICT_3X3_32 custom'}
        for name in aruco.__dict__:
            if name.startswith('DICT_'):
                dicts[aruco.__dict__[name]] = name
        return sorted(list(zip(dicts.keys(), dicts.values())))

    def check_params(self):
        """ check command line params

            :return: False in case of parameter error
        """
        if not self.args.names:
            print("no input images given", file=sys.stderr)
            return False
        if self.args.input:
            if not os.path.isfile(self.args.input) or \
               not os.access(self.args.input, os.R_OK):
                print(f'cannot open input file {self.args.input}', file=sys.stderr)
                return False
        return True

    def coo_input(self):
        """ load world coordinates of GCPs
            input file format: point_id easting northing elevation
            coordinates are stored in coords dict
        """
        with open(self.args.input, 'r', encoding="ascii") as finput:
            for line in finput:
                co_list = line.strip().split(args.separator)
                if len(co_list) < 4:
                    print(f"Illegal input: {line}", file=sys.stderr)
                    continue
                # check coordinates are numerical?
                try:
                    _ = [float(x) for x in co_list[1:4]]
                except ValueError:
                    print("Non-numerical coordinates: {line}", file=sys.stderr)
                # store original precision of coordinates
                self.coords[int(co_list[0])] = co_list[1:4]

    def process_images(self):
        """ process all images """
        # process image files from command line
        for f_name in self.args.names:
            # read actual image file
            if self.args.verbose:
                print(f"processing {f_name}", file=sys.stderr)
            self.process_image(f_name)
        if self.args.verbose:
            for j, k in self.gcp_found.items():
                print(f'GCP{j}: on {len(k)} images {k}', file=sys.stderr)
        self.gcp_output()

    def process_image(self, image_name):
        """ proces single image

            :param image_name: path to image to process
        """
        if 'dng' in image_name.lower():
            dng = DngFile.read(image_name)
            frame = dng.postprocess()  # demosaicing by rawpy
        else :
            frame = cv2.imread(image_name)
        if frame is None:
            print(f'error reading image: {image_name}', file=sys.stderr)
            return
        # convert image to gray
        if self.args.adjust:
            # adjust colors for better recognition
            tmp = cv2.LUT(frame, self.lut)
            gray = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # find markers
        if packaging.version.parse(cv2.__version__) < packaging.version.parse('4.8'):
            corners, ids, _ = aruco.detectMarkers(gray,
                                                  self.aruco_dict,
                                                  parameters=self.params)
        else:
            detector = aruco.ArucoDetector(self.aruco_dict, self.params)
            corners, ids, _ = detector.detectMarkers(gray)
        if ids is None:
            print(f'No markers found on image {image_name}', file=sys.stderr)
            return
        # check duplicate ids
        idsl = [pid[0] for pid in ids]
        if len(ids) - len(set(idsl)):
            print(f'duplicate markers on image {image_name}\nmarker ids: {sorted(idsl)}', file=sys.stderr)
        # calculate center & output found markers
        if self.args.verbose:
            print(f'  {ids.size} GCP markers found', file=sys.stderr)
        if self.args.debug:  # show found ids in debug mode
            plt.figure()
            plt.title(f"{len(ids)} GCP, {len(ids) - len(set(idsl))} duplicate found on {image_name}")
            # show markers on original image
            aruco.drawDetectedMarkers(gray, corners, ids)
            plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        for i in range(ids.size):
            j = ids[i][0]
            if j not in self.gcp_found:
                self.gcp_found[j] = []
            self.gcp_found[j].append(image_name)
            # calculate center of aruco code
            x = int(round(np.average(corners[i][0][:, 0])))
            y = int(round(np.average(corners[i][0][:, 1])))
            if args.basename :
                self.gcps.append((x, y, os.path.basename(image_name), j, corners[i][0]))
            else :
                self.gcps.append((x, y, os.path.abspath(image_name), j, corners[i][0]))


            if self.args.debug:
                if j in self.coords:
                    plt.plot(x, y, args.markerstyle, markersize=self.args.markersize,
                                                     markeredgecolor=args.edgecolor, markeredgewidth=args.edgewidth)
                else:
                    plt.plot(x, y, args.markerstyle1, markersize=self.args.markersize,
                             markeredgecolor=args.edgecolor, markeredgewidth=args.edgewidth)
                plt.text(x+self.args.markersize, y, str(ids[i][0]),
                         color=args.fontcolor1, weight=args.fontweight1, fontsize=args.fontsize)
                plt.text(x+self.args.markersize, y, str(ids[i][0]),
                         color=args.fontcolor, weight=args.fontweight, fontsize=args.fontsize)
        if args.debug:
            #plt.legend()
            plt.show()

    def gcp_output(self):
        """ output GPCs to output file """
        if self.args.output == sys.stdout:
            foutput = self.args.output
        else:
            try:
                foutput = open(self.args.output, 'w', encoding="ascii")
            except Exception:
                print('cannot open output file', file=sys.stderr)
                return
        if self.args.type == 'ODM' and self.args.epsg is not None:
            # write epsg code to the beginning of the output
            foutput.write(f'EPSG:{self.args.epsg}\n')

        for gcp in self.gcps:
            j = gcp[3]
            if self.args.type == 'ODM':
                if j in self.coords:
                    if len(self.gcp_found[j]) <= self.args.limit:
                        foutput.write(f"{self.coords[j][0]} {self.coords[j][1]} {self.coords[j][2]} {gcp[0]} {gcp[1]} {gcp[2]} {j}\n")
                        # .format( self.coords[j][0], self.coords[j][1], self.coords[j][2], gcp[0], gcp[1], gcp[2], j))
                    else:
                        print(f"GCP {j} over limit it is dropped on image {gcp[2]}", file=sys.stderr)
                else:
                    print(f"No coordinates for {j}", file=sys.stderr)
            elif self.args.type == 'VisualSfM':
                if j in self.coords:
                    if len(self.gcp_found[j]) <= self.args.limit:
                        foutput.write(f"{gcp[2]} {gcp[0]} {gcp[1]} {self.coords[j][0]} {self.coords[j][1]} {self.coords[j][2]} {j}\n")
                        #.format( gcp[2], gcp[0], gcp[1], self.coords[j][0], self.coords[j][1], self.coords[j][2], j))
                    else:
                        print(f"GCP {j} over limit it is dropped on image {gcp[2]}", file=sys.stderr)
                else:
                    print(f"No coordinates for {j}", file=sys.stderr)
            elif self.args.type == 'Meshroom':
                if j in self.coords:
                    if len(self.gcp_found[j]) <= self.args.limit:
                        corners = gcp[4]
                        tl = corners[2]
                        bl = corners[1]
                        br = corners[0]
                        tr = corners[3]

                        max_sides = max(norm(tl-bl), norm(bl-br), norm(br-tr), norm(tr-tl))
                        max_diagonal = max(0.707*norm(tl-br), 0.707*norm(tr-bl))

                        size = 0.5 * max(max_sides, max_diagonal)

                        foutput.write(f"{gcp[0]} {gcp[1]} {gcp[2]} {j} {size:.4f}\n")
                        #.format( gcp[0], gcp[1], gcp[2], j, size))
                    else:
                        print(f"GCP {j} over limit it is dropped on image {gcp[2]}", file=sys.stderr)
                else:
                    print(f"No coordinates for {j}", file=sys.stderr)
            else:
                if j in self.coords:
                    if len(self.gcp_found[j]) <= self.args.limit:
                        foutput.write(f"{self.coords[j][0]} {self.coords[j][1]} {self.coords[j][2]} {gcp[0]} {gcp[1]} {gcp[2]} {j}\n")
                        # .format( self.coords[j][0], self.coords[j][1], self.coords[j][2], gcp[0], gcp[1], gcp[2], j))
                    else:
                        print(f"GCP {j} over limit it is dropped on image {gcp[2]}", file=sys.stderr)
                else:
                    if len(self.gcp_found[j]) <= self.args.limit:
                        foutput.write(f"{gcp[0]} {gcp[1]} {gcp[2]} {j}\n")
                        # .format( gcp[0], gcp[1], gcp[2], j))
                    else:
                        print(f"GCP {j} over limit it is dropped on image {gcp[2]}", file=sys.stderr)
        if self.args.output != sys.stdout:
            foutput.close()

def cmd_params(parser, params):
    """ set up command line argument parser

        :param parser: command line parser object
        :param params: ArUco parameters for defaults
    0"""
    def_dict = aruco.DICT_4X4_100   # default dictionary 4X4
    def_output = sys.stdout         # default output to stdout
    def_input = None                # default no input coordinates
    def_separator = " "             # default separator is space
    def_type = ""                   # default output type
    def_markersize = 10             # marker size of debug image
    def_markerstyle = "ro"          # marker style with GCP coords
    def_markerstyle1 = "r^"          # marker style without GCP coords
    def_edgecolor = "y"             # edge color for markers
    def_edgewidth = 3               # edge width for markers
    def_fontsize = 6                # marker size of debug image
    def_fontcolor = 'r'             # inner color for GP ID annotation
    def_fontcolor1 = 'y'            # outer color for GP ID annotation
    def_fontweight = 'normal'       # weight for inner text
    def_fontweight1 = 'bold'        # weight for outet text
    def_limit = 999                 # limit for individual id records in output

    parser.add_argument('names', metavar='file_names', type=str, nargs='*',
                        help='image files to process')
    # general parameters
    parser.add_argument('-d', '--dict', type=int, default=def_dict,
                        help=f'marker dictionary id, default={def_dict} (DICT_4X4_100)')
    parser.add_argument('-o', '--output', type=str, default=def_output,
                        help='name of output GCP list file, default stdout')
    parser.add_argument('-t', '--type', choices=['ODM', 'VisualSfM', 'Meshroom'],
                        default=def_type,
                        help=f'target program ODM or VisualSfM, default {def_type}')
    parser.add_argument('-i', '--input', type=str, default=def_input,
                        help=f'name of input GCP coordinate file, default {def_input}')
    parser.add_argument('-s', '--separator', type=str, default=def_separator,
                        help=f'input file separator, default {def_separator}')
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='verbose output to stdout')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--debug', action="store_true",
                       help='show detected markers on image')
    parser.add_argument('-l', '--list', action="store_true",
                        help='output dictionary names and ids and exit')
    parser.add_argument('--epsg', type=int, default=None,
                        help='epsg code for gcp coordinates, default None')
    parser.add_argument('-a', '--adjust', action="store_true",
                        help='adjust colors by built in lookup table')
    # parameters for marker display
    parser.add_argument('--markersize', type=int, default=def_markersize,
                        help='marker size on debug image, use together with debug')
    parser.add_argument('--markerstyle', type=str, default=def_markerstyle,
                        help='marker style for point with coordinates, use together with debug')
    parser.add_argument('--markerstyle1', type=str, default=def_markerstyle1,
                        help='marker style for point without coordinates, use together with debug')
    parser.add_argument('--edgecolor', type=str, default=def_edgecolor,
                        help='marker edge color, use together with debug')
    parser.add_argument('--edgewidth', type=int, default=def_edgewidth,
                        help='marker edge width, use together with debug')
    parser.add_argument('--fontsize', type=int, default=def_fontsize,
                        help='font size on debug image, use together with debug')
    parser.add_argument('--fontcolor', type=str, default=def_fontcolor,
                        help='inner font color on debug image, use together with debug')
    parser.add_argument('--fontcolor1', type=str, default=def_fontcolor1,
                        help='outer font color on debug image, use together with debug')
    parser.add_argument('--fontweight', type=str, default=def_fontweight,
                        help='inner font weight on debug image, use together with debug')
    parser.add_argument('--fontweight1', type=str, default=def_fontweight1,
                        help='outer font weight on debug image, use together with debug')
    parser.add_argument('--limit', type=int, default=def_limit,
                        help='limit the number of records in the output for a unique id')
    # parameters for ArUco detection
    parser.add_argument('--aruco_params', type=str, default=None,
                        help='all ArUco detection parameters are read from a JSON file, other ArUco detection parameters are ignored from the command line')
    parser.add_argument('--thres', type=float,
                        default=params.adaptiveThreshConstant,
                        help=f'adaptive threshold constant, default {params.adaptiveThreshConstant}')
    parser.add_argument('--winmax', type=int,
                        default=params.adaptiveThreshWinSizeMax,
                        help=f'adaptive thresholding window max size, default {params.adaptiveThreshWinSizeMax}')
    parser.add_argument('--winmin', type=int,
                        default=params.adaptiveThreshWinSizeMin,
                        help=f'adaptive tresholding window min size, default {params.adaptiveThreshWinSizeMin}')
    parser.add_argument('--winstep', type=int,
                        default=params.adaptiveThreshWinSizeStep,
                        help=f'adaptive thresholding window size step , default {params.adaptiveThreshWinSizeStep}')
    parser.add_argument('--maxiter', type=int,
                        default=params.cornerRefinementMaxIterations,
                        help=f'Stop criteria for subpixel process, default {params.cornerRefinementMaxIterations}')
    parser.add_argument('--refinement', type=int,
                        default=params.cornerRefinementMethod,
                        help=f'Subpixel process method, default {params.cornerRefinementMethod}')
    parser.add_argument('--minacc', type=float,
                        default=params.cornerRefinementMinAccuracy,
                        help=f'Stop criteria for subpixel process, default {params.cornerRefinementMinAccuracy}')
    parser.add_argument('--refwin', type=int,
                        default=params.cornerRefinementWinSize,
                        help=f'Window size for subpixel refinement, default {params.cornerRefinementWinSize}')
    parser.add_argument('-r', '--inverted', action="store_true",
                        help=f'detect inverted markers, default {params.detectInvertedMarker}')
    parser.add_argument('--correctionrate', type=float,
                        default=params.errorCorrectionRate,
                        help=f'max error correction, default {params.errorCorrectionRate}')
    parser.add_argument('--borderbits', type=int,
                        default=params.markerBorderBits,
                        help=f'width of marker border, default {params.markerBorderBits}')
    parser.add_argument('--error', type=float,
                        default=params.maxErroneousBitsInBorderRate,
                        help=f'Border bits error rate, default {params.maxErroneousBitsInBorderRate}')
    parser.add_argument('--maxrate', type=float,
                        default=params.maxMarkerPerimeterRate,
                        help=f'max marker perimeter rate, default {params.maxMarkerPerimeterRate}')
    parser.add_argument('--corner', type=float,
                        default=params.minCornerDistanceRate,
                        help=f'minimum distance any pair of corners in the same marker, default {params.minCornerDistanceRate}')
    parser.add_argument('--borderdist', type=int,
                        default=params.minDistanceToBorder,
                        help=f'minimum distance any marker corner to image border, default {params.minDistanceToBorder}')
    parser.add_argument('--markerdist', type=float,
                        default=params.minMarkerDistanceRate,
                        help=f'minimum distance any pair of corners from different markers, default {params.minMarkerDistanceRate}')
    parser.add_argument('--lengthratio', type=float,
                        default=params.minMarkerLengthRatioOriginalImg,
                        help=f'range [0,1], default {params.minMarkerLengthRatioOriginalImg}')
    parser.add_argument('--minrate', type=float,
                        default=params.minMarkerPerimeterRate,
                        help=f'min marker perimeter rate, default {params.minMarkerPerimeterRate}')
    parser.add_argument('--otsu', type=float, default=params.minOtsuStdDev,
                        help=f'minimum stddev of pixel values, default {params.minOtsuStdDev}')
    # TODO minSideLengthCanonicalImg missing
    parser.add_argument('--ignore', type=float,
                        default=params.perspectiveRemoveIgnoredMarginPerCell,
                        help=f'Ignored pixels at cell borders, default {params.perspectiveRemoveIgnoredMarginPerCell}')
    parser.add_argument('--persp', type=int,
                        default=params.perspectiveRemovePixelPerCell,
                        help=f'number of pixels per cells, default {params.perspectiveRemovePixelPerCell}')
    parser.add_argument('--poly', type=float,
                        default=params.polygonalApproxAccuracyRate,
                        help=f'polygonal approx accuracy rate, default {params.polygonalApproxAccuracyRate}')
    parser.add_argument('--aruco3', action="store_true",
                        help=f'use ArUco3 detection, default {params.useAruco3Detection}')
    parser.add_argument('--basename', action="store_true", default=False,
                        help='basename for image files')

if __name__ == "__main__":
    T1 = time.perf_counter()
    # set up command line argument parser
    params = aruco.DetectorParameters()
    parser = argparse.ArgumentParser()
    cmd_params(parser, params)
    # parse command line arguments
    args = parser.parse_args()
    if os.name == "nt":
        # extend wildcards on indows
        names = []
        for name in args.names:
            names += glob.glob(name)
        args.names = names
    gcps = GcpFind(args, params)
    gcps.process_images()
    T2 = time.perf_counter()
    print(f'Finished in {T2-T1} seconds', file=sys.stderr)
