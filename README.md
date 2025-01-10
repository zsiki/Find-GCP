# Find-GCP
Find ArUco markers in digital photos

![](https://raw.githubusercontent.com/zsiki/Find-GCP/master/fgcp_logo.png#50x50)

This project is maintained by the [GeoForAll Lab](http://www.agt.bme.hu/osgeolab/index.php?page=start&lang=en) at the [Department of Geodesy and Surveying](http://geod.bme.hu/geod/hirek?language=en) of the Budapest University of Technology and Economics.

A paper is available about this project in the Baltic Journal of Modern Computing Vol 9. (2021) No.1 [Automatic Recognition of ArUco Codes in Land Surveying Tasks](https://www.bjmc.lu.lv/fileadmin/user_upload/lu_portal/projekti/bjmc/Contents/9_1_06_Siki.pdf).

[The project page on OpenHub](https://www.openhub.net/p/Find-GCP)

## News

- New command line switch (--aruco\_params) to specify all ArUco command line parameters in a JSON file
- New output format parameter to generate GCP file for Meshroom
- The Python 2.x compatibility is not maintened after 08/27/2003.

## Installation

[ArUco markers](http://chev.me/arucogen) are black and white square markers which have unique pattern and ID. [OpenCV](https://opencv.org) library has a modul to find ArUco markers in images.

### Pipenv installation
Pipenv should be installed. [Instructions here](https://github.com/pypa/pipenv?tab=readme-ov-file#installation)

### Clone the repo
Clone the Find-GCP GitHub repo or download the zip file

```
git clone https://github.com/zsiki/Find-GCP.git
```
or
```
wget https://github.com/zsiki/Find-GCP/archive/refs/heads/master.zip
unzip master.zip
```
You can also download zip using the **Code** button on the GitHub page of the project.

### Dependencies installations
Go to the Find-GCP directory and then :

```
pipenv install
```


## Preparing ArUco markers

Before taking the photos the different ArUco markers have to be printed in the suitable size and put on the field. The coordinates of markers have to be measured by GNSS (GPS), total station or other surveyor's method. We prefer the 3x3 or 4x4 ArUco library, the larger the squares in the marker, the smaller the the total marker size can be. You should print markers on gray background to avoid burt in of white on photos. You can use [gsd_calc](http://www.agt.bme.hu/on_line/gsd_calc/gsd_calc.html) utitility to estimate necessary marker size from the sensor parameters and fligth altitude.

The 3x3 or 4x4 ArUco markers on the image should be minimum 20 x 20 pixels to be detected, the optimal marker size is 30 x 30 pixels. You should plan the marker size depending on the flight altitude and camera parameters. For example 30 x 30 cm markers are enough for a DJI Phantom 4P flying 50 m above the ground.

When you fix your markers on the field please let enough space around the outer black border. For example do not put stones near to the black border of the marker. The software cannot separate them and the marker won't be recognised. The left side marker was not recognised on the following image, because of the two stones at the upper left and right corners. On the right side image the gray spots were removed and recognized.

![Clear border](https://raw.githubusercontent.com/zsiki/Find-GCP/master/samples/fixing.png)

Figure 1 Non-clear and clear border

## Usage
Before using the scripts virtualenv should be ativated with

```
pipenv shell
```

### gcp_find.py

This small utility can be used together with photogrammetric programs like Open Drone Map or WebODM to create the necessary Ground Control Point (GCP) file containing image coordinates and projected coordinates of GCPs. It has command line interface (CLI) only. There are several parameters:

```
usage: gcp_find.py [-h] [-d DICT] [-o OUTPUT] [-t {ODM,VisualSfM}] [-i INPUT]
                   [-s SEPARATOR] [-v] [--debug] [-l] [--epsg EPSG] [-a]
                   [--markersize MARKERSIZE] [--markerstyle MARKERSTYLE]
                   [--markerstyle1 MARKERSTYLE1] [--edgecolor EDGECOLOR]
                   [--edgewidth EDGEWIDTH] [--fontsize FONTSIZE]
                   [--fontcolor FONTCOLOR] [--fontcolor1 FONTCOLOR1]
                   [--fontweight FONTWEIGHT] [--fontweight1 FONTWEIGHT1]
                   [--limit LIMIT] [--aruco_params ARUCO_PARAMS]
                   [--thres THRES] [--winmax WINMAX] [--winmin WINMIN]
                   [--winstep WINSTEP] [--maxiter MAXITER]
                   [--refinement REFINEMENT] [--minacc MINACC]
                   [--refwin REFWIN] [-r] [--correctionrate CORRECTIONRATE]
                   [--borderbits BORDERBITS] [--error ERROR]
                   [--maxrate MAXRATE] [--corner CORNER]
                   [--borderdist BORDERDIST] [--markerdist MARKERDIST]
                   [--lengthratio LENGTHRATIO] [--minrate MINRATE]
                   [--otsu OTSU] [--ignore IGNORE] [--persp PERSP]
                   [--poly POLY] [--aruco3]
                   [file_names ...]

positional arguments:
  file_names            image files to process

options:
  -h, --help            show this help message and exit
  -d DICT, --dict DICT  marker dictionary id, default=1 (DICT_4X4_100)
  -o OUTPUT, --output OUTPUT
                        name of output GCP list file, default stdout
  -t {ODM,VisualSfM,Meshroom}, --type {ODM,VisualSfM,Meshroom}
                        target program ODM or VisualSfM, default
  -i INPUT, --input INPUT
                        name of input GCP coordinate file, default None
  -s SEPARATOR, --separator SEPARATOR
                        input file separator, default
  -v, --verbose         verbose output to stdout
  --debug               show detected markers on image
  -l, --list            output dictionary names and ids and exit
  --epsg EPSG           epsg code for gcp coordinates, default None
  -a, --adjust          adjust colors by built in lookup table
  --markersize MARKERSIZE
                        marker size on debug image, use together with debug
  --markerstyle MARKERSTYLE
                        marker style for point with coordinates, use together
                        with debug
  --markerstyle1 MARKERSTYLE1
                        marker style for point without coordinates, use
                        together with debug
  --edgecolor EDGECOLOR
                        marker edge color, use together with debug
  --edgewidth EDGEWIDTH
                        marker edge width, use together with debug
  --fontsize FONTSIZE   font size on debug image, use together with debug
  --fontcolor FONTCOLOR
                        inner font color on debug image, use together with
                        debug
  --fontcolor1 FONTCOLOR1
                        outer font color on debug image, use together with
                        debug
  --fontweight FONTWEIGHT
                        inner font weight on debug image, use together with
                        debug
  --fontweight1 FONTWEIGHT1
                        outer font weight on debug image, use together with
                        debug
  --limit LIMIT         limit the number of records in the output for a unique
                        id
  --aruco_params ARUCO_PARAMS
                        all ArUco detection parameters are read from a JSON
                        file, other ArUco detection parameters are ignored
                        from the command line
  --thres THRES         adaptive threshold constant, default 7.0
  --winmax WINMAX       adaptive thresholding window max size, default 23
  --winmin WINMIN       adaptive tresholding window min size, default 3
  --winstep WINSTEP     adaptive thresholding window size step , default 10
  --maxiter MAXITER     Stop criteria for subpixel process, default 30
  --refinement REFINEMENT
                        Subpixel process method, default 0
  --minacc MINACC       Stop criteria for subpixel process, default 0.1
  --refwin REFWIN       Window size for subpixel refinement, default 5
  -r, --inverted        detect inverted markers, default False
  --correctionrate CORRECTIONRATE
                        max error correction, default 0.6
  --borderbits BORDERBITS
                        width of marker border, default 1
  --error ERROR         Border bits error rate, default 0.35
  --maxrate MAXRATE     max marker perimeter rate, default 4.0
  --corner CORNER       minimum distance any pair of corners in the same
                        marker, default 0.05
  --borderdist BORDERDIST
                        minimum distance any marker corner to image border,
                        default 3
  --markerdist MARKERDIST
                        minimum distance any pair of corners from different
                        markers, default 0.05
  --lengthratio LENGTHRATIO
                        range [0,1], default 0.0
  --minrate MINRATE     min marker perimeter rate, default 0.03
  --otsu OTSU           minimum stddev of pixel values, default 5.0
  --ignore IGNORE       Ignored pixels at cell borders, default 0.13
  --persp PERSP         number of pixels per cells, default 4
  --poly POLY           polygonal approx accuracy rate, default 0.03
  --aruco3              use ArUco3 detection, default False
```

List of the available dictionary codes (see --list):

```
0 : DICT_4X4_50
1 : DICT_4X4_100
2 : DICT_4X4_250
3 : DICT_4X4_1000
4 : DICT_5X5_50
5 : DICT_5X5_100
6 : DICT_5X5_250
7 : DICT_5X5_1000
8 : DICT_6X6_50
9 : DICT_6X6_100
10 : DICT_6X6_250
11 : DICT_6X6_1000
12 : DICT_7X7_50
13 : DICT_7X7_100
14 : DICT_7X7_250
15 : DICT_7X7_1000
16 : DICT_ARUCO_ORIGINAL
17 : DICT_APRILTAG_16h5
18 : DICT_APRILTAG_25h9
19 : DICT_APRILTAG_36h10
20 : DICT_APRILTAG_36h11
21 : DICT_ARUCO_MIP_36H12
99 : DICT_3X3_32 custom
```

Parameters from *winmax* to *aruco3* are customizable parameters for ArUco detection and are explaned in the OpenCV [Aruco documentation](https://docs.opencv.org/trunk/d5/dae/tutorial_aruco_detection.html). The two most important parameters are *minrate* and *ignore*. Usually the default values of these parameters are not perfect.

*minrate* defines the minimal size of a marker in a relative way. For example if the larger image size is 5472 pixels and the *minrate* parameter is 0.01, then the minimal perimeter of an ArUco marker should be 0.01 \* 5472 = 54 pixels, and the minimal size of the marker side is 54 / 4 = 13 pixels. Smaller marker candidates are dropped. Our exprerience is the minimal marker side should be 20-30 pixels to detect 4x4 markers. Using the special 3x3 markers (see: dict\_gen\_3x3.py) the size of the marker can be reduced. So you can calculate marker size in centimetres if you know the pixel size in centimetres, in case of 30-50 metres flight altitude, it is 1-2 cm (DJI Phantom Pro). You should use 20-40 cm large markers.

*ignore* is also a relative value. It defines the percent of pixels to ignore at the border of the elemens of the marker matrix. In strong sunshine the white areas are burnt on the image. A 0.33 value (33%) is good for burnt images, the green squares on figure below will be used to detect black/white elements. There is an other solution to reduce the burnt effect, use grey paper to print the aruco codes. The second figure below shows the original black/grey marker and the marker on the image. Thanks to the adaptive thresholding in the ArUco module, grey and black can be separated. *adjust* can also be used to reduce the effect of white burnt in.

![burnt in effect](https://raw.githubusercontent.com/zsiki/Find-GCP/master/samples/burnt.png)

Figure 2 Burnt in effect and the --ignore

![gray black marker](https://raw.githubusercontent.com/zsiki/Find-GCP/master/samples/grey_black.png)

Figure 3 Burnt in effect reduced by black/grey marker. Original marker left, marker on image right.

Sample imput file for GCP coordinates (pointID easting northing elevation):

```
0 650544.828 237514.298 104.215
1 650552.086 237521.011 104.129
2 650546.305 237521.605 104.217
3 650534.729 237526.552 104.267
4 650542.850 237532.382 104.165
5 650553.513 237514.344 104.169
6 650552.275 237505.909 104.196
```

See our publication in Baltic Journal of Modern Computing:
[Automatic Recognition of ArUco Codes in Land Surveying Tasks](https://www.bjmc.lu.lv/fileadmin/user_upload/lu_portal/projekti/bjmc/Contents/9_1_06_Siki.pdf)

Marker detection is not perfect, there may be false pozitive matches and some markers couldn't be
detected. Please use *gcp_check.py* utility to make a quick visual check.
The smaller the internal matrix of ArUco marker the higher the chance for false matche.

![false_match](https://raw.githubusercontent.com/zsiki/Find-GCP/master/samples/false_match.png)

Fugure 4 False match and the original found marker


### Utilities

There are some small utilities in this repo, too.

#### exif\_pos.py

This small program lists GPS position from exif information of images to the standard output. You can redirect standard output to a file and load it for example into QGIS as delimited text layer to show image positions.

```
Usage: ./exif_pos.py image_file(s)
```

Sample output of the program:

```
./exif_pos.py *.JPG
DJI_0021.JPG,19.120939,47.683572,203.86
DJI_0022.JPG,19.120958,47.683647,203.86
DJI_0023.JPG,19.120985,47.683718,203.86
DJI_0024.JPG,19.121020,47.683821,203.76
DJI_0025.JPG,19.121042,47.683890,203.76
DJI_0026.JPG,19.121080,47.683997,203.76
DJI_0038.JPG,19.120905,47.684089,203.76
DJI_0039.JPG,19.120872,47.683985,203.76
DJI_0040.JPG,19.120846,47.683917,203.76
DJI_0041.JPG,19.120786,47.683741,203.86
DJI_0042.JPG,19.120762,47.683671,203.86
DJI_0043.JPG,19.120725,47.683566,203.86
```

#### aruco\_make.py

It generates aruco marker images of different standard and 3x3 non-standard dictionaries for printing.

```
usage: aruco_make.py [-h] [-d DICT] [-s START] [-e END] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -d DICT, --dict DICT  marker dictionary id (use 99 for 3x3 markers),
                        default= 1 (DICT_4X4_100)
  -s START, --start START
                        first marker to generate, default= 0
  -e END, --end END     last marker to generate, default= -1
  -v, --view            show marker on monitor
  -g, --gray            generate black/gray marker
  --value VALUE         shade of background use with --gray, default=95
  -p PAD, --pad PAD     border width around marker in inches, default= 0.5
```

You can also use Romain Basile's [GCP Aruco Marker Generator](https://github.com/gromain/gcp_aruco_generator) to get SVG markers.

#### gcp\_check.py

gcp\_check.py is a GUI application which helps the visual check of the found GCPs by gcp\_find.py.
It has several command line parameters and a simple menu. The output file of the gcp\_find.py is the input
file of this program. There are forward and backward buttons to step between images. Mouse wheel can be
used to zoom in/out and left button to pan.

```
usage: gcp_check.py [-h] [--command COMMAND] [--path PATH] [-s SEPARATOR]
                    [--markersize MARKERSIZE] [--edgecolor EDGECOLOR]
                    [--edgewidth EDGEWIDTH] [--fontsize FONTSIZE]
                    [--fontcolor FONTCOLOR]
                    [file_name]

positional arguments:
  file_name             GCP file to process

optional arguments:
  -h, --help            show this help message and exit
  --command COMMAND     command all/ID show all images/images with GCP ID
  --path PATH           input path for images
  -s SEPARATOR, --separator SEPARATOR
                        input file separator, default
  --markersize MARKERSIZE
                        marker size on image, default 200
  --edgecolor EDGECOLOR
                        marker edge color, default red
  --edgewidth EDGEWIDTH
                        marker edge width, default 20
  --fontsize FONTSIZE   font size on image, default 200
  --fontcolor FONTCOLOR
                        font color on image, default red
```

![original_image](https://raw.githubusercontent.com/zsiki/Find-GCP/master/samples/orig.png)

![marked_gcps](https://raw.githubusercontent.com/zsiki/Find-GCP/master/samples/gcps.png)

Figure 5 Original image and found GCPs marked

#### gsd\_cal

gsd\_calc is a simple web application written in JavaScript using jQuery to estimate the Ground Sample Distance (GSD) and the ArUco markes size depending on
the sensor data and flight altitude.

There is a small database (realy a JSON file) with the parameters of some cameras. There are three obligatory and two optional parameters in it.

-**focal** focal length of the camera in mm
-**iheight** image height in pixels (optional)
-**iwidth** image width in pixels
-**sheight** sensor width in mm
-**swidth** sensor height in mm (optional)

It is available on line [here](http://www.agt.bme.hu/on_line/gsd_calc/gsd_calc.html).

## Samples

Images used in the samples are available in the *samples* directory. Please share with us your samples using *gcp_find*.

### Sample 1

Find ArUco markers in an image and output marker IDs and image coordinates of marker centers.

```
./gcp_find.py samples/markers.png

502 342 markers.png 16
328 342 markers.png 15
152 342 markers.png 14
502 142 markers.png 13
328 142 markers.png 12
152 142 markers.png 11
```

### Sample 2

We have 3 images made by DJI Phantom 4 Pro. Coordinates of GCPs were measured by GNSS and stored in [A3.txt](samples/A3.txt) file. The 3x3 ArUco markers were used
The next command will generate the necessary text file for ODM.

```
./gcp_find.py -v -t ODM -i samples/A3.txt --epsg 23700 -o samples/gcp_list.txt --minrate 0.01 --ignore 0.33 -d 99 samples/DJI_017[234].JPG

processing samples/DJI_0172.JPG
duplicate markers on image samples/DJI_0172.JPG
marker ids: [2, 3, 4, 8, 9, 9]
  6 GCP markers found
processing samples/DJI_0173.JPG
  5 GCP markers found
processing samples/DJI_0174.JPG
  8 GCP markers found
GCP9: on 4 images ['samples/DJI_0172.JPG', 'samples/DJI_0172.JPG', 'samples/DJI_0173.JPG', 'samples/DJI_0174.JPG']
GCP8: on 3 images ['samples/DJI_0172.JPG', 'samples/DJI_0173.JPG', 'samples/DJI_0174.JPG']
GCP3: on 3 images ['samples/DJI_0172.JPG', 'samples/DJI_0173.JPG', 'samples/DJI_0174.JPG']
GCP4: on 3 images ['samples/DJI_0172.JPG', 'samples/DJI_0173.JPG', 'samples/DJI_0174.JPG']
GCP2: on 3 images ['samples/DJI_0172.JPG', 'samples/DJI_0173.JPG', 'samples/DJI_0174.JPG']
GCP1: on 1 images ['samples/DJI_0174.JPG']
GCP0: on 1 images ['samples/DJI_0174.JPG']
GCP10: on 1 images ['samples/DJI_0174.JPG']
No coordinates for 10
```

The gcp_list.txt output file which is ready for use with ODM or WebODM. Copy the gcp_list.txt into your images directory using ODM and add the

```
    --gcp ./images/gcp_list.txt
```

switch to your ODM command. In case of WebODM upload gcp_list.txt file with your images.

The gcp_list.txt file should look like:

```
EPSG:23700
650530.705 237530.488 104.066 3206 2391 DJI_0172.JPG 9
650538.926 237536.529 104.113 1952 2323 DJI_0172.JPG 8
650534.729 237526.552 104.267 3124 1703 DJI_0172.JPG 3
650542.850 237532.382 104.165 1908 1622 DJI_0172.JPG 4
650546.305 237521.605 104.217 2419 368 DJI_0172.JPG 2
650530.705 237530.488 104.066 188 2010 DJI_0172.JPG 9
650530.705 237530.488 104.066 3172 2413 DJI_0173.JPG 9
650538.926 237536.529 104.113 1921 2343 DJI_0173.JPG 8
650534.729 237526.552 104.267 3091 1727 DJI_0173.JPG 3
650542.850 237532.382 104.165 1880 1644 DJI_0173.JPG 4
650546.305 237521.605 104.217 2393 396 DJI_0173.JPG 2
650530.705 237530.488 104.066 3535 2892 DJI_0174.JPG 9
650538.926 237536.529 104.113 2287 2838 DJI_0174.JPG 8
650534.729 237526.552 104.267 3444 2206 DJI_0174.JPG 3
650542.850 237532.382 104.165 2236 2136 DJI_0174.JPG 4
650546.305 237521.605 104.217 2725 879 DJI_0174.JPG 2
650552.086 237521.011 104.129 2239 403 DJI_0174.JPG 1
650544.828 237514.298 104.215 3408 322 DJI_0174.JPG 0
```

Alternatively you can set all ArUco marker recognition parameters from a
JSON file using --aruco_params switch. It is enough to set parameters where default is not
suitable. If you create the following JSON file (aruco_params.json)

```
{
    "minMarkerPerimeterRate" : 0.01,
    "perspectiveRemoveIgnoredMarginPerCell" : 0.33
}
```

then you can change the command line:

```
./gcp_find.py -v -t ODM -i samples/A3.txt --epsg 23700 -o samples/gcp_list.txt --aruco_params aruco_params.json -d 99 samples/DJI_017[234].JPG
```

### Sample 3

Photos (DJI0087.jpg and DJI0088.jpg) made by a DJI Phantom 4 Pro. There are three 4x4 GCPs (id=3, id=4, id=5) on image DJI\_0087.jpg and five (id=0, id=3, id=4, id=5, id=6) on image DJI\_0088.jpg.

```
python3 gcp_find.py --minrate 0.01 samples/bme/DJI_008[78].jpg

2832 1844 DJI_0087.jpg 5
1963 1764 DJI_0087.jpg 4
2472 732 DJI_0087.jpg 3
3024 3556 DJI_0088.jpg 5
2654 2458 DJI_0088.jpg 3
2448 1315 DJI_0088.jpg 0
3094 1300 DJI_0088.jpg 6
```

### Sample 4

Photos (DJI\_0180.jpg and DJI\_0181.jpg) made by DJI Phantom 4 Pro, flying alttitude 50 m. There are eight 3x3 black/grey GCPs on image DJI\_0180.png and ten on
DJI\_0181.png.

```
python3 gcp_find.py -d 99 --minrate 0.01 --ignore 0.33 samples/bme/DJI_018[01].jpg

duplicate markers on image samples/bme/DJI_0180.jpg
marker ids: [0, 1, 1, 2, 3, 4, 5, 6, 7, 28]
3459 3250 DJI_0180.jpg 3
2700 3229 DJI_0180.jpg 4
2982 2414 DJI_0180.jpg 2
2664 2113 DJI_0180.jpg 1
2644 1038 DJI_0180.jpg 7
3402 2042 DJI_0180.jpg 0
2879 1655 DJI_0180.jpg 5
3328 1214 DJI_0180.jpg 6
2982 2409 DJI_0180.jpg 28
2584 64 DJI_0180.jpg 1
3671 2746 DJI_0181.jpg 9
2897 2733 DJI_0181.jpg 8
3602 2322 DJI_0181.jpg 3
2850 2299 DJI_0181.jpg 4
3128 1502 DJI_0181.jpg 2
2812 1208 DJI_0181.jpg 1
3545 1138 DJI_0181.jpg 0
2792 153 DJI_0181.jpg 7
241 1618 DJI_0181.jpg 31
3026 758 DJI_0181.jpg 5
3471 327 DJI_0181.jpg 6
2070 418 DJI_0181.jpg 15
```

At 2584,64 on image DJI_0180.jpg is a false match.

### Sample 5

Using the same images as [Sample 2](#sample-2), the following command shows an example of the Meshroom output. This file can be used in Meshroom with the [GCP marker additions](https://github.com/MrClock8163/MeshroomGCPMarkerAdditions).

```
./gcp_find.py -t Meshroom -i samples/A3.txt -o samples/gcp_list.txt --minrate 0.01 --ignore 0.33 -d 99 samples/DJI_017[234].JPG

duplicate markers on image samples/DJI_0172.JPG
marker ids: [2, 3, 4, 8, 9, 9]
No coordinates for 10
```

The gcp_list.txt should look like:

```
3206 2391 DJI_0172.JPG 9 17.0000
1952 2323 DJI_0172.JPG 8 16.7643
3124 1703 DJI_0172.JPG 3 16.5303
1908 1622 DJI_0172.JPG 4 16.5076
2419 368 DJI_0172.JPG 2 16.5680
188 2010 DJI_0172.JPG 9 56.6414
3172 2413 DJI_0173.JPG 9 16.5076
1921 2343 DJI_0173.JPG 8 16.5303
3091 1727 DJI_0173.JPG 3 16.5303
1880 1644 DJI_0173.JPG 4 16.5303
2393 396 DJI_0173.JPG 2 16.5303
3535 2892 DJI_0174.JPG 9 16.5000
2287 2838 DJI_0174.JPG 8 17.0294
3444 2206 DJI_0174.JPG 3 16.5303
2236 2136 DJI_0174.JPG 4 16.5076
2725 879 DJI_0174.JPG 2 16.5303
2239 403 DJI_0174.JPG 1 16.0078
3408 322 DJI_0174.JPG 0 16.0312
```

The First two columns contain the position of the ArUco marker, the third is
the name of the image file, the fourth is the ID of the market, the fifth is
the half of the size of max(side, diagonal).
