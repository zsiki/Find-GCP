#! /usr/bin/python
# -*- coding: utf-8 -*-
""" Ceate special 3x3 (32) ArUco dictionary in subfolde "dict_3x3"
"""
import cv2
import os

aruco = cv2.aruco
if os.path.exists('dict_3x3'):
    if not os.path.isdir('dict_3x3'):
        print('"dict_3x3" is not a folder')
        exit(1)
else:
    try:
        os.mkdir('dict_3x3')
    except:
        print('cannot create "dict_3x3" folder')
        exit(2)
d = cv2.aruco.Dictionary_create(32, 3)  # aruco 3x3 dictionary
for i in range(32):
    marker = cv2.aruco.drawMarker(d, i, 256)  # create marker
    # create image file from marker
    cv2.imwrite('dict_3x3/3x3_{}.png'.format(i), marker)
