#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
    visual check tool for gcp_find.py
    (c) Zoltan Siki siki (dot) zoltan (at) epito.bme.hu
"""

import argparse
import re
from os import path
import matplotlib.pyplot as plt
import cv2

class GcpCheck():
    """ class to check found GCPs visually """

    def __init__(self, gcp_file, gcp_style, separator=" ", img_path=''):
        """ initialize

            :param gcp_file: output file of gcp_find.py
            :param gcp_style: command line parameters
            :param separator: field separator in CGP file, default space
            :param img_path: path to images if it is not in the same folder as CGP file
            :param gcp_params: parameters for GCP markers
        """
        self.gcp_file = gcp_file
        self.style = gcp_style
        self.separator = separator
        self.img_path = img_path
        # load GCP file
        self.LoadGcps()

    def LoadGcps(self):
        """ Load GCP image coordinates and image names

            list of GCP data is generated, each item in the list contains
            image x, y, image name and GCP ID
            A list is also generated with image names
        """
        self.gcps = []
        imgs = set()
        with open(self.gcp_file) as fp:
            for line in fp:
                fields = line.strip("\n\r").split(self.separator)
                if len(fields) > 3:
                    self.gcps.append([int(fields[-4]), int(fields[-3]),
                                     fields[-2], int(fields[-1])])
                    imgs.add(fields[-2])
        self.imgs = sorted(list(imgs))

    def ShowImage(self, img_name, gcp_id=None):
        """ show an image with GCPs

            :param img_name: image to display
        """
        plt.figure()
        if gcp_id is None:
            title = img_name
        else:
            title = "{} id={}".format(img_name, gcp_id)
        plt.title(title)
        img_path = img_name
        if not path.exists(img_name):
            img_path = path.join(self.img_path, img_name)
        if not path.exists(img_path):
            img_path = path.join(path.split(self.gcp_file)[0], img_name)
        frame = cv2.imread(img_path)
        if frame is not None:
            plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        for gcp in self.gcps:
            if gcp[2] == img_name:
                plt.plot(gcp[0], gcp[1], self.style['markerstyle'],
                         markersize=self.style['markersize'],
                         markeredgecolor=self.style['edgecolor'],
                         markeredgewidth=self.style['edgewidth'])
                plt.text(gcp[0]+self.style['markersize'], gcp[1], gcp[-1],
                         color=self.style['fontcolor1'],
                         weight=self.style['fontweight1'],
                         fontsize=self.style['fontsize'])
                plt.text(gcp[0]+self.style['markersize'], gcp[1], gcp[-1],
                         color=self.style['fontcolor'],
                         weight=self.style['fontweight'],
                         fontsize=self.style['fontsize'])
        plt.show()

    def ShowAll(self):
        """ Show alll images """
        for img in self.imgs:
            self.ShowImage(img)

    def ShowId(self, gcp_id):
        """ Show images with GCP id

            :param gcp_id: GCP id
        """
        # collect image names with id
        imgs = set()
        for gcp in self.gcps:
            if gcp[-1] == gcp_id:
                imgs.add(gcp[-2])
        for img in sorted(list(imgs)):
            self.ShowImage(img, gcp_id)

def cmd_params(parser):
    """ handle command line parameters

        :param parser: command line parser
    """
    def_separator = " "             # default separator is space
    def_markersize = 10             # marker size of debug image
    def_markerstyle = "ro"          # marker style for GCP
    def_edgecolor = "y"             # edge color for markers
    def_edgewidth = 3               # edge width for markers
    def_fontsize = 16               # marker size of debug image
    def_fontcolor = 'r'             # inner color for GP ID annotation
    def_fontcolor1 = 'y'            # outer color for GP ID annotation
    def_fontweight = 'normal'       # weight for inner text
    def_fontweight1 = 'bold'        # weight for outet text

    parser.add_argument('name', metavar='file_name', type=str, nargs=1,
                        help='GCP file to process')
    parser.add_argument('--command', type=str, default='all',
                        help='command all/ID show all images/images with GCP ID')
    parser.add_argument('--path', type=str, default='',
                        help='input path for images')
    parser.add_argument('-s', '--separator', type=str, default=def_separator,
                        help='input file separator, default {}'.format(def_separator))

    # parameters for marker display
    parser.add_argument('--markersize', type=int, default=def_markersize,
                        help='marker size on image, default {}'.format(def_markersize))
    parser.add_argument('--markerstyle', type=str, default=def_markerstyle,
                        help='marker style for GCPs, default "{}"'.format(def_markerstyle))
    parser.add_argument('--edgecolor', type=str, default=def_edgecolor,
                        help='marker edge color, default {}'.format(def_edgecolor))
    parser.add_argument('--edgewidth', type=int, default=def_edgewidth,
                        help='marker edge width, default {}'.format(def_edgewidth))
    parser.add_argument('--fontsize', type=int, default=def_fontsize,
                        help='font size on image, default {}'.format(def_fontsize))
    parser.add_argument('--fontcolor', type=str, default=def_fontcolor,
                        help='inner font color on image, default {}'.format(def_fontcolor))
    parser.add_argument('--fontcolor1', type=str, default=def_fontcolor1,
                        help='outer font color on image, default {}'.format(def_fontcolor1))
    parser.add_argument('--fontweight', type=str, default=def_fontweight,
                        help='inner font weight on image, default {}'.format(def_fontweight))
    parser.add_argument('--fontweight1', type=str, default=def_fontweight1,
                        help='outer font weight on image, default {}'.format(def_fontweight1))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmd_params(parser)
    args = parser.parse_args()
    style = {'markersize': args.markersize,
             'markerstyle': args.markerstyle,
             'edgecolor': args.edgecolor,
             'edgewidth': args.edgewidth,
             'fontsize': args.fontsize,
             'fontcolor': args.fontcolor,
             'fontcolor1': args.fontcolor1,
             'fontweight': args.fontweight,
             'fontweight1': args.fontweight1}

    gcp_c = GcpCheck(args.name[0], style, args.separator, args.path)
    if args.command == "all":
        gcp_c.ShowAll()
    elif re.match("^[0-9]+$", args.command):
        gcp_c.ShowId(int(args.command))
    else:
        gcp_c.ShowImage(args.command)
