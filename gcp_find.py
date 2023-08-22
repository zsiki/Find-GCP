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
import argparse
from multiprocessing import Pool, cpu_count
import numpy as np
import matplotlib.pyplot as plt
import cv2
from cv2 import aruco

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
            self.aruco_dict = aruco.Dictionary(32, 3)
        else:
            self.aruco_dict = aruco.getPredefinedDictionary(args.dict)

        # set aruco parameters from command line arguments
        self.params = params
        self.params.detectInvertedMarker = args.inverted
        self.params.adaptiveThreshWinSizeMin = args.winmin
        self.params.adaptiveThreshWinSizeMax = args.winmax
        self.params.adaptiveThreshWinSizeStep = args.winstep
        self.params.adaptiveThreshConstant = args.thres
        self.params.minMarkerPerimeterRate = args.minrate
        self.params.maxMarkerPerimeterRate = args.maxrate
        self.params.polygonalApproxAccuracyRate = args.poly
        self.params.minCornerDistanceRate = args.corner
        self.params.minMarkerDistanceRate = args.markerdist
        self.params.minDistanceToBorder = args.borderdist
        self.params.markerBorderBits = args.borderbits
        self.params.minOtsuStdDev = args.otsu
        self.params.perspectiveRemovePixelPerCell = args.persp
        self.params.perspectiveRemoveIgnoredMarginPerCell = args.ignore
        self.params.maxErroneousBitsInBorderRate = args.error
        self.params.errorCorrectionRate = args.correct
        self.params.cornerRefinementMethod = args.refinement
        self.params.cornerRefinementWinSize = args.refwin
        self.params.cornerRefinementMaxIterations = args.maxiter
        self.params.cornerRefinementMinAccuracy = args.minacc
        if self.args.list:
            # list available aruco dictionary names & exit
            for act_dict in self.list_dicts():
                print('{} : {}'.format(act_dict[0], act_dict[1]), file=sys.stderr)
            # list all aruco parameters
            for par in dir(self.params):
                if not par.startswith('__'):
                    val = getattr(self.params, par)
                    if type(val) in (int, float, str, bool):
                        print('{} : {}'.format(par, val), file=sys.stderr)
            sys.exit(0)

        self.coords = {}
        if self.args.nez:
            self.east = 0   # position of east coordinate in input
            self.north = 1  # position of north coordinate in input
        else:
            self.east = 0   # position of east coordinate in input
            self.north = 1  # position of north coordinate in input
        self.elev = 2   # position of elevation in input
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
        dict_list = [(99, 'DICT_3X3_32 custom')]
        for name in aruco.__dict__:
            if name.startswith('DICT_'):
                dict_list.append((aruco.__dict__[name], name))
        return sorted(dict_list)

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
                print('cannot open input file {}'.format(self.args.input), file=sys.stderr)
                return False
        return True

    def coo_input(self):
        """ load world coordinates of GCPs
            input file format: point_id easting northing elevation
            coordinates are stored in coords dict
        """
        with open(self.args.input, 'r') as finput:
            for line in finput:
                co_list = line.strip().split(self.args.separator)
                if len(co_list) < 4:
                    print("Illegal input: {}".format(line), file=sys.stderr)
                    continue
                # coords are stored as strings to preserve precision
                self.coords[int(co_list[0])] = co_list[1:4]

    def process_images(self):
        """ process all images """
        # process image files from command line
        if self.args.multi:
            pool = Pool(processes=cpu_count())
            self.gcps = filter(None, list(pool.map(self.process_image, self.args.names)))
        else:
            self.gcps = filter(None, list(map(self.process_image, self.args.names)))
        #for f_name in self.args.names:
            # read actual image file
        #    if self.args.verbose:
        #        print("processing {}".format(f_name), file=sys.stderr)
        #    self.gcps += self.process_image(f_name)
        if self.args.verbose:
            for j in self.gcp_found:
                print('GCP{}: on {} images {}'.format(j, len(self.gcp_found[j]),
                                                      self.gcp_found[j]), file=sys.stderr)

    def process_image(self, image_name):
        """ proces single image

            :param image_name: path to image to process
        """
        gcps = []
        if self.args.verbose:
            print("processing {}".format(image_name), file=sys.stderr)
        frame = cv2.imread(image_name)
        if frame is None:
            print('error reading image: {}'.format(image_name), file=sys.stderr)
            return None
        # convert image to gray
        if self.args.adjust:
            # adjust colors for better recognition
            tmp = cv2.LUT(frame, self.lut)
            gray = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
        else:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # find markers
        corners, ids, _ = aruco.detectMarkers(gray,
                                              self.aruco_dict,
                                              parameters=self.params)
        if ids is None:
            print('No markers found on image {}'.format(image_name), file=sys.stderr)
            return None
        # check duplicate ids
        idsl = [pid[0] for pid in ids]
        if len(ids) - len(set(idsl)):
            print('duplicate markers on image {}\nmarker ids: {}'.format(image_name, sorted(idsl)), file=sys.stderr)
        # calculate center & output found markers
        if self.args.verbose:
            print('  {} GCP markers found'.format(ids.size), file=sys.stderr)
        if self.args.debug:  # show found ids in debug mode
            plt.figure()
            plt.title("{} GCP, {} duplicate found on {}".format(len(ids), len(ids) - len(set(idsl)), image_name))
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
            gcps.append((x, y, os.path.basename(image_name), j))
            if self.args.debug:
                if j in self.coords:
                    plt.plot(x, y, self.args.markerstyle, markersize=self.args.markersize,
                             markeredgecolor=self.args.edgecolor, markeredgewidth=self.args.edgewidth)
                else:
                    plt.plot(x, y, self.args.markerstyle1, markersize=self.args.markersize,
                             markeredgecolor=self.args.edgecolor, markeredgewidth=args.edgewidth)
                plt.text(x+self.args.markersize, y, str(ids[i][0]),
                         color=self.args.fontcolor1, weight=self.args.fontweight1, fontsize=self.args.fontsize)
                plt.text(x+self.args.markersize, y, str(ids[i][0]),
                         color=self.args.fontcolor, weight=self.args.fontweight, fontsize=self.args.fontsize)
        if self.args.debug:
            #plt.legend()
            plt.show()
        return gcps

    def gcp_output(self):
        """ output GPCs to output file """
        if self.args.output == sys.stdout:
            foutput = self.args.output
        else:
            try:
                foutput = open(self.args.output, 'w')
            except Exception:
                print('cannot open output file', file=sys.stderr)
                return
        if self.args.type == 'ODM' and self.args.epsg is not None:
            # write epsg code to the beginning of the output
            foutput.write('EPSG:{}\n'.format(self.args.epsg))

        for gcp_list in self.gcps:
            for gcp in gcp_list:
                j = gcp[3]
                if self.args.type == 'ODM':
                    if j in self.coords:
                        if len(self.gcp_found[j]) <= self.args.limit:
                            foutput.write('{} {} {} {} {} {} {}\n'.format(
                                self.coords[j][self.east],
                                self.coords[j][self.north],
                                self.coords[j][self.elev],
                                gcp[0], gcp[1], gcp[2], j))
                        else:
                            print("GCP {} over limit it is dropped on image {}".format(
                                j, gcp[2]), file=sys.stderr)
                    else:
                        print("No coordinates for {}".format(j), file=sys.stderr)
                elif self.args.type == 'VisualSfM':
                    if j in self.coords:
                        if len(self.gcp_found[j]) <= self.args.limit:
                            foutput.write('{} {} {} {} {} {} {}\n'.format(
                                gcp[2], gcp[0], gcp[1],
                                self.coords[j][self.east], self.coords[j][self.north],
                                self.coords[j][self.elev], j))
                        else:
                            print("GCP {} over limit it is dropped on image {}".format(
                                j, gcp[2]), file=sys.stderr)
                    else:
                        print("No coordinates for {}".format(j), file=sys.stderr)
                else:
                    if j in self.coords:
                        if len(self.gcp_found[j]) <= self.args.limit:
                            foutput.write('{} {} {} {} {} {} {}\n'.format(
                                self.coords[j][self.east], self.coords[j][self.north],
                                self.coords[j][self.elev], gcp[0], gcp[1], gcp[2], j))
                        else:
                            print("GCP {} over limit it is dropped on image {}".format(
                                j, gcp[2]), file=sys.stderr)
                    else:
                        if len(self.gcp_found[j]) <= self.args.limit:
                            foutput.write('{} {} {} {}\n'.format(
                                gcp[0], gcp[1], gcp[2], j))
                        else:
                            print("GCP {} over limit it is dropped on image {}".format(
                                j, gcp[2]), file=sys.stderr)
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
                        help='marker dictionary id, default={} (DICT_4X4_100)'
                        .format(def_dict))
    parser.add_argument('-o', '--output', type=str, default=def_output,
                        help='name of output GCP list file, default stdout')
    parser.add_argument('-t', '--type', choices=['ODM', 'VisualSfM'],
                        default=def_type,
                        help='target program ODM or VisualSfM, default {}'
                        .format(def_type))
    parser.add_argument('-i', '--input', type=str, default=def_input,
                        help='name of input GCP coordinate file, default {}'
                        .format(def_input))
    parser.add_argument('-s', '--separator', type=str, default=def_separator,
                        help='input file separator, default {}'
                        .format(def_separator))
    parser.add_argument('-v', '--verbose', action="store_true",
                        help='verbose output to stdout')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--debug', action="store_true",
                       help='show detected markers on image')
    group.add_argument('--multi', action="store_true",
                       help='process images paralel')
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
    parser.add_argument('--nez', action="store_true",
                        help='set the coordinate order in GCP input to North,East,Elevation (compatible with GCPEditorPro)')
    # parameters for ArUco detection
    parser.add_argument('-r', '--inverted', action="store_true",
                        help='detect inverted markers')
    parser.add_argument('--winmin', type=int,
                        default=params.adaptiveThreshWinSizeMin,
                        help='adaptive tresholding window min size, default {}'
                        .format(params.adaptiveThreshWinSizeMin))
    parser.add_argument('--winmax', type=int,
                        default=params.adaptiveThreshWinSizeMax,
                        help='adaptive thresholding window max size, default {}'
                        .format(params.adaptiveThreshWinSizeMax))
    parser.add_argument('--winstep', type=int,
                        default=params.adaptiveThreshWinSizeStep,
                        help='adaptive thresholding window size step , default {}'
                        .format(params.adaptiveThreshWinSizeStep))
    parser.add_argument('--thres', type=float,
                        default=params.adaptiveThreshConstant,
                        help='adaptive threshold constant, default {}'
                        .format(params.adaptiveThreshConstant))
    parser.add_argument('--minrate', type=float,
                        default=params.minMarkerPerimeterRate,
                        help='min marker perimeter rate, default {}'
                        .format(params.minMarkerPerimeterRate))
    parser.add_argument('--maxrate', type=float,
                        default=params.maxMarkerPerimeterRate,
                        help='max marker perimeter rate, default {}'
                        .format(params.maxMarkerPerimeterRate))
    parser.add_argument('--poly', type=float,
                        default=params.polygonalApproxAccuracyRate,
                        help='polygonal approx accuracy rate, default {}'
                        .format(params.polygonalApproxAccuracyRate))
    parser.add_argument('--corner', type=float,
                        default=params.minCornerDistanceRate,
                        help='minimum distance any pair of corners in the same marker, default {}'
                        .format(params.minCornerDistanceRate))
    parser.add_argument('--markerdist', type=float,
                        default=params.minMarkerDistanceRate,
                        help='minimum distance any pair of corners from different markers, default {}'
                        .format(params.minMarkerDistanceRate))
    parser.add_argument('--borderdist', type=int,
                        default=params.minDistanceToBorder,
                        help='minimum distance any marker corner to image border, default {}'
                        .format(params.minDistanceToBorder))
    parser.add_argument('--borderbits', type=int,
                        default=params.markerBorderBits,
                        help='width of marker border, default {}'
                        .format(params.markerBorderBits))
    parser.add_argument('--otsu', type=float, default=params.minOtsuStdDev,
                        help='minimum stddev of pixel values, default {}'
                        .format(params.minOtsuStdDev))
    parser.add_argument('--persp', type=int,
                        default=params.perspectiveRemovePixelPerCell,
                        help='number of pixels per cells, default {}'
                        .format(params.perspectiveRemovePixelPerCell))
    parser.add_argument('--ignore', type=float,
                        default=params.perspectiveRemoveIgnoredMarginPerCell,
                        help='Ignored pixels at cell borders, default {}'
                        .format(params.perspectiveRemoveIgnoredMarginPerCell))
    parser.add_argument('--error', type=float,
                        default=params.maxErroneousBitsInBorderRate,
                        help='Border bits error rate, default {}'
                        .format(params.maxErroneousBitsInBorderRate))
    parser.add_argument('--correct', type=float,
                        default=params.errorCorrectionRate,
                        help='Bit correction rate, default {}'
                        .format(params.errorCorrectionRate))
    parser.add_argument('--refinement', type=int,
                        default=params.cornerRefinementMethod,
                        help='Subpixel process method, default {}'
                        .format(params.cornerRefinementMethod))
    parser.add_argument('--refwin', type=int,
                        default=params.cornerRefinementWinSize,
                        help='Window size for subpixel refinement, default {}'
                        .format(params.cornerRefinementWinSize))
    parser.add_argument('--maxiter', type=int,
                        default=params.cornerRefinementMaxIterations,
                        help='Stop criteria for subpixel process, default {}'
                        .format(params.cornerRefinementMaxIterations))
    parser.add_argument('--minacc', type=float,
                        default=params.cornerRefinementMinAccuracy,
                        help='Stop criteria for subpixel process, default {}'
                        .format(params.cornerRefinementMinAccuracy))

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
    if args.multi:
        args.multi = False
        print("WAENING -- Multi processing is not available yet")
    gcps = GcpFind(args, params)
    gcps.process_images()
    gcps.gcp_output()
    T2 = time.perf_counter()
    print(f'Finished in {T2-T1} seconds', file=sys.stderr)
