#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
""" calibrate camera using charuco board 7x5
"""
import sys
import argparse
import yaml
import numpy as np
import cv2

parser = argparse.ArgumentParser()
parser.add_argument('names', metavar='file_names', type=str, nargs='*',
                    help='board images from diffirent directions to process')
parser.add_argument('-b', '--board', action="store_true",
                    help='save only board image to charuco.png file')
parser.add_argument('-c', '--camera', action="store_true",
                    help='use first camera to take photos')
parser.add_argument('-s', '--save', action="store_true",
                    help='save camera images to file cal0.png, cal1.png if camera is used')
parser.add_argument('-o', '--output', type=str,
                    default="calibration_matrix.yaml",
                    help='output yaml camera calibration data file, default: calibration_matrix.yaml')

args = parser.parse_args()
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
board = cv2.aruco.CharucoBoard_create(5, 7, .025, .0125, dictionary)
img = board.draw((200 * 5, 200 * 7))

if args.board:
    #Dump the calibration board to a file
    cv2.imwrite('charuco.png', img)
    sys.exit()

if not args.names and not args.camera:
    print("neither camera nor input images given")
    parser.print_help()
    sys.exit(0)

allCorners = []
allIds = []
decimator = 0

if args.camera:
    #Start capturing images for calibration
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, dictionary)

        if ids is not None and len(ids) > 0:
            ret, corners1, ids1 = cv2.aruco.interpolateCornersCharuco(corners,
                                                                      ids,
                                                                      gray,
                                                                      board)
            cv2.aruco.drawDetectedMarkers(gray, corners, ids)

        cv2.imshow('frame', gray)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        if key == 13:
            if corners1 is not None and ids1 is not None and len(ids1) > 3:
                allCorners.append(corners1)
                allIds.append(ids1)
            if args.save:
                fn = "cal{:d}.png".format(decimator)
                cv2.imwrite(fn, frame)
            decimator += 1
else:
    # load images from files
    for fn in args.names:
        # read images from files
        frame = cv2.imread(fn)
        if frame is None:
            print('error reading image: {}'.format(fn))
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, dictionary)
        if ids is not None and len(ids) > 0:
            ret, corners1, ids1 = cv2.aruco.interpolateCornersCharuco(corners,
                                                                      ids,
                                                                      gray,
                                                                      board)
            if ret > 2:
                allCorners.append(corners1)
                allIds.append(ids1)
                decimator += 1

imsize = gray.shape

#Calibration fails for lots of reasons. Release the video if we do
try:
    ret, mtx, dist, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(allCorners,
                                                                    allIds,
                                                                    board,
                                                                    imsize,
                                                                    None,
                                                                    None)
except:
    if args.camera:
        cap.release()
    print('Calibration failed')
    sys.exit(1)

if args.camera:
    cap.release()
    cv2.destroyAllWindows()
# transform matrix and distortion to writeable lists
cal = {'camera_matrix': np.asarray(mtx).tolist(),
       'dist_coeff': np.asarray(dist).tolist()}
# and save to file
with open(args.output, "w") as f:
    yaml.dump(cal, f)
print(cal)
