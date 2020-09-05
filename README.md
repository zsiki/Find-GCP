# Find-GCP
Find ArUco markers in digital photos

[ArUco markers](http://chev.me/arucogen) are black and white square markers 
which have unique pattern and ID. [OpenCV](https://opencv.org) library has
a modul to find ArUco markers in images (you should pip install 
*opencv-python* and *opencv-contrib-python*).

Before taking the photos the different ArUco markers have to be printed in the
suitable size and put on the field. The coordinates of markers have to be
measured by GNSS (GPS), total station or other surveyor's method. We prefer the
3x3 or 4x4 ArUco library, the larger the squares in the marker, the smaller the 
the total marker size can be.

The 3x3 or 4x4 ArUco markers on the image should be minimum 20 x 20 pixels to be
detected, the optimal
marker size is 30 x 30 pixels. You should plan the marker size depending on the 
flight altitude and camera parameters. For example 30 x 30 cm markers are enough
for a DJI Phantom 4P flying 50 m above the ground.

This small utility can be used together with photogrammetric programs like Open
Drone Map or WebODM to create the necessary Ground Control Point (GCP) file 
containing image coordinates and projected coordinates of GCPs. 
It has command line interface (CLI) only. There ore 

```
usage: gcp_find.py [-h] [-d DICT] [-o OUTPUT] [-t {ODM,VisualSfM}] [-i INPUT]
                   [-s SEPARATOR] [-v] [-r] [--debug] [--winmin WINMIN]
                   [--winmax WINMAX] [--winstep WINSTEP] [--thres THRES]
                   [--minrate MINRATE] [--maxrate MAXRATE] [--poly POLY]
                   [--corner CORNER] [--markerdist MARKERDIST]
                   [--borderdist BORDERDIST] [--borderbits BORDERBITS]
                   [--otsu OTSU] [--persp PERSP] [--ignore IGNORE]
                   [--error ERROR] [--correct CORRECT]
                   [--refinement REFINEMENT] [--refwin REFWIN]
                   [--maxiter MAXITER] [--minacc MINACC] [-l]
                   [file_names [file_names ...]]

positional arguments:
  file_names            image files to process

optional arguments:
  -h, --help            show this help message and exit
  -d DICT, --dict DICT  marker dictionary id, default=1 (DICT_4X4_100)
  -o OUTPUT, --output OUTPUT
                        name of output GCP list file, default stdout
  -t {ODM,VisualSfM}, --type {ODM,VisualSfM}
                        target program ODM or VisualSfM, default ODM
  -i INPUT, --input INPUT
                        name of input GCP coordinate file, default None
  -s SEPARATOR, --separator SEPARATOR
                        input file separator, default
  -v, --verbose         verbose output to stdout
  -r, --inverted        detect inverted markers
  --debug               show rejected and detected markers on image
  --winmin WINMIN       adaptive tresholding window min size, default 3
  --winmax WINMAX       adaptive thresholding window max size, default 23
  --winstep WINSTEP     adaptive thresholding window size step , default 10
  --thres THRES         adaptive threshold constant, default 7.0
  --minrate MINRATE     min marker perimeter rate, default 0.03
  --maxrate MAXRATE     max marker perimeter rate, default 4.0
  --poly POLY           polygonal approx accuracy rate, default 0.03
  --corner CORNER       minimum distance any pair of corners in the same
                        marker, default 0.05
  --markerdist MARKERDIST
                        minimum distance any pair of corners from different
                        markers, default 0.05
  --borderdist BORDERDIST
                        minimum distance any marker corner to image border,
                        default 3
  --borderbits BORDERBITS
                        width of marker border, default 1
  --otsu OTSU           minimum stddev of pixel values, default 5.0
  --persp PERSP         number of pixels per cells, default 4
  --ignore IGNORE       Ignored pixels at cell borders, default 0.13
  --error ERROR         Border bits error rate, default 0.35
  --correct CORRECT     Bit correction rate, default 0.6
  --refinement REFINEMENT
                        Subpixel process method, default 0
  --refwin REFWIN       Window size for subpixel refinement, default 5
  --maxiter MAXITER     Stop criteria for subpixel process, default 30
  --minacc MINACC       Stop criteria for subpixel process, default 0.1
  -l, --list            output dictionary names and ids and exit
```

Parameters from *winmin* to *minacc* are customizable parameters for ArUco detection
and are explaned in the OpenCV 
[Aruco documentation](https://docs.opencv.org/trunk/d5/dae/tutorial_aruco_detection.html).
The two most important parameters are *minrate* and *ignore*. Usually the 
default values of these parameters are not perfect.

*minrate* defines the minimal size of a marker in a relative way. For example if
the larger image size is 5472 pixels and the *minrate* parameter is 0.01, then the
minimal perimeter of an ArUco marker should be 0.01 \* 5472 = 54 pixels, and the
minimal size of the marker side is 54 / 4 = 13 pixels. Smaller marker candidates 
are dropped. Our exprerience is the minimal marker side should be 20-30 pixels
to detect 4x4 markers. Using the special 3x3 markers (see: dict\_gen\_3x3.py)
the size of the marker can be reduced.
So you can calculate marker size in centimetres if you know
the pixel size in centimetres, in case of 30-50 metres flight altitude, it is
1-2 cm (DJI Phantom Pro). You should use 20-40 cm large markers.

*ignore* is also a relative value. It defines the percent of pixels to ignore 
at the border of the elemens of the marker matrix. In strong sunshine the white
areas are burnt on the image. A 0.33 value (33%) is good for burnt images, the
green squares on the image below.  There is an other solution to reduce the
burnt effect, use grey paper to print the aruco codes. The second figure below
shows the original black/grey marker and the marker on the image. Thanks to the
adaptive thresholding in the ArUco module, grey and black can be separated.

![burnt in effect](samples/burnt.png)
Burnt in effect and the --ignore

![gray black marker](samples/grey_black.png)
Burnt in effect reduced by black/grey marker

There are some small utilities in this repo, too.

* exif\_pos.py list GPS position from exif information of images
* dict\_gen\_3x3.py generate 32 custom 3x3 ArUco dictionary in dict_3x3 subdirectory (png files)
* aruco\_make.py generate aruco markers of different dictionaries

## Sample 1

Find ArUco markers in an image and output marker IDs and image coordinates of marker centers.

```
python3 gcp_find.py samples/markers.png

16 502 342 markers.png
15 328 342 markers.png
14 152 342 markers.png
13 502 142 markers.png
12 328 142 markers.png
11 152 142 markers.png
```
![found markers](samples/found_markers.png)

## Sample 2

Coordinates of GCPs were measured by total station and stored in
[aruco.txt](samples/aruco.txt) file. These GCPs should be used in ODM or WebODM.
The next command will generate the necessary text file for ODM.

<img src="samples/20191029_110429.jpg" alt="img1" width="400"/> <img src="samples/20191029_110437.jpg" alt="img2" width="400"/>

```
python3 gcp\_find.py -v -i samples/aruco.txt -o test.txt samples/2019*.jpg
Loading GCP coordinates from samples/aruco.txt
processing samples/20191029_110429.jpg
  5 GCP markers found
processing samples/20191029_110437.jpg
  6 GCP markers found
GCP6: on 2 images ['samples/20191029_110429.jpg', 'samples/20191029_110437.jpg']
GCP5: on 2 images ['samples/20191029_110429.jpg', 'samples/20191029_110437.jpg']
GCP4: on 2 images ['samples/20191029_110429.jpg', 'samples/20191029_110437.jpg']
GCP1: on 2 images ['samples/20191029_110429.jpg', 'samples/20191029_110437.jpg']
GCP3: on 2 images ['samples/20191029_110429.jpg', 'samples/20191029_110437.jpg']
GCP2: on 1 images ['samples/20191029_110437.jpg']
```
The test.txt output file
```
1.041 3.712 -0.560 204 3051 20191029_110429.jpg
4.119 3.764 -0.518 3658 2886 20191029_110429.jpg
2.173 4.202 -0.153 1639 2487 20191029_110429.jpg
4.482 4.201 0.370 3852 1981 20191029_110429.jpg
2.822 4.201 0.359 2311 1978 20191029_110429.jpg
4.482 4.201 0.370 4069 2075 20191029_110437.jpg
2.822 4.201 0.359 2514 2064 20191029_110437.jpg
1.041 3.712 -0.560 462 3160 20191029_110437.jpg
5.758 3.859 -0.557 5302 3001 20191029_110437.jpg
4.119 3.764 -0.518 3853 3017 20191029_110437.jpg
2.173 4.202 -0.153 1848 2566 20191029_110437.jpg
```

Note: You have to add [projection parameters](https://docs.opendronemap.org/tutorials.html#ground-control-points) at the beginning of the file to use it with ODM or WebODM.

## Sample 3

Photos (DJI0087.jpg and DJI0088.jpg) made by a DJI Phantom 4 Pro.
There are three 4x4 GCPs (id=3, id=4, id=5) on image DJI\_0087.jpg and five
(id=0, id=3, id=4, id=5, id=6) on image DJI\_0088.jpg.

```
python3 gcp_find.py --minrate 0.01 samples/bme/DJI_008[78].jpg

5 2832 1845 DJI_0087.jpg
3 2472 731 DJI_0087.jpg
5 3024 3556 DJI_0088.jpg
3 2654 2458 DJI_0088.jpg
0 2448 1315 DJI_0088.jpg
6 3094 1299 DJI_0088.jpg
```

Marker 4 not detected.

## Sample 4

Photos (DJI\_0180.jpg and DJI\_0181.jpg) made by DJI Phantom 4 Pro, flying
alttitude 50 m.
There are eight 3x3 black/grey GCPs on image DJI\_0180.png and ten on 
DJI\_0181.png.

```
python3 gcp_find.py -d 99 --minrate 0.01 --ignore 0.33 samples/bme/DJI_018[01].jpg 
3 3458 3251 DJI_0180.jpg
4 2700 3229 DJI_0180.jpg
2 2981 2414 DJI_0180.jpg
1 2663 2114 DJI_0180.jpg
7 2644 1038 DJI_0180.jpg
0 3401 2042 DJI_0180.jpg
5 2879 1655 DJI_0180.jpg
6 3328 1214 DJI_0180.jpg
9 3671 2746 DJI_0181.jpg
8 2897 2733 DJI_0181.jpg
3 3602 2322 DJI_0181.jpg
4 2850 2299 DJI_0181.jpg
2 3128 1502 DJI_0181.jpg
1 2812 1207 DJI_0181.jpg
0 3545 1138 DJI_0181.jpg
7 2792 152 DJI_0181.jpg
5 3026 758 DJI_0181.jpg
6 3471 327 DJI_0181.jpg
```

All markers found.
