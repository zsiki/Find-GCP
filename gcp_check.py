#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
    visual check tool for gcp_find.py
    (c) Zoltan Siki siki (dot) zoltan (at) emk.bme.hu
"""

import argparse
from os import path
import os
import sys
import tkinter as tk
from tkinter import Tk, ttk
from tkinter import messagebox
from tkinter import filedialog
import pandas as pd
import PIL
import PIL.ImageDraw
import PIL.ImageTk
import PIL.ImageFont
from PIL import Image

from matplotlib import font_manager
from process_raw import DngFile

class AutoScrollbar(ttk.Scrollbar):
    """ A scrollbar that hides itself if it's not needed.
        Works only if you use the grid geometry manager
    """
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with this widget')

    def place(self, **kw):
        raise tk.TclError('Cannot use place with this widget')

class GcpCheck(tk.Tk):
    """ class to check found GCPs visually """

    def __init__(self, gcp_style, gcp_file=None, separator=" ", width=700, height=550,
                 img_path='./'):
        """ initialize

            :param gcp_file: output file of gcp_find.py
            :param gcp_style: GCP marker style parameters
            :param separator: field separator in CGP file, default space
            :param width: initial window width
            :param height: initial window height
            :param img_path: path to images if it is not in the same folder as CGP file
        """
        tk.Tk.__init__(self)

        #__import__("IPython").embed()

        self.title("Image Viewer")
        self.geometry(f"{width}x{height}")
        # add menu
        self.menu = tk.Menu(master=self)
        self.fileMenu = tk.Menu(self.menu, tearoff=0)
        self.fileMenu.add_command(label="Open", command=self.SelectFile)
        self.fileMenu.add_command(label="Exit", command=exit)
        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.config(menu=self.menu)
        self.image = None
        self.button_back = tk.Button(self, text="<-", command=self.back)
        self.button_forward = tk.Button(self, text="->", command=self.forward)
        self.button_back.grid(row=0, column=0, sticky='w')
        self.button_forward.grid(row=0, column=2, sticky='e')
        # scrollbars
        vbar = AutoScrollbar(self, orient='vertical')
        hbar = AutoScrollbar(self, orient='horizontal')
        vbar.grid(row=1, column=4, sticky='ns')
        hbar.grid(row=2, column=0, sticky='we')
        self.canvas = tk.Canvas(self, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set,
                                width=width, height=height/2)
        self.canvas.grid(row=1, column=0, columnspan=3, sticky='nswe')
        self.canvas.update()  # wait till canvas is created
        vbar.configure(command=self.scroll_y)  # bind scrollbars to the canvas
        hbar.configure(command=self.scroll_x)
        # Make the canvas expandable
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.canvas.bind('<Configure>', self.ShowImage)  # canvas is resized
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up

        self.gcp_file = gcp_file
        self.style = gcp_style
        self.separator = separator
        self.width = None
        self.height = None
        self.img_path = img_path
        self.imscale = 1.0  # scale for the canvaas image
        self.delta = 1.3    # zoom magnitude
        # load GCP file
        self.gcps = []
        self.imgs = []
        self.img_no = 0
        self.orig_img = None
        self.img = None
        font = font_manager.FontProperties(family='sans-serif', weight='normal')
        font_file = font_manager.findfont(font)
        self.font = PIL.ImageFont.truetype(font_file, size=self.style["fontsize"])
        self.bind("<Configure>",self.ShowImage)
        if self.gcp_file and self.LoadGcps():
            self.ShowImage()
    def SelectFile(self):
        self.gcp_file = filedialog.askopenfilename()
        if self.gcp_file and self.LoadGcps():
            self.ShowImage()

    def LoadGcps(self):
        """ Load GCP image coordinates and image names

            pandas data frame is created
            a sorted list is also generated with image names
        """
        retry = True
        skiprows =0

         # Check if the file exists
        if not os.path.isfile(self.gcp_file):
            print(f"The file {self.gcp_file} does not exist.")
            sys.exit()

        # Attempt to read the first line to verify CSV structure
        try:
            # Open the file and read a sample to check for valid CSV structure
            with open(self.gcp_file, 'r', encoding='utf-8') as csv_file:
                # Check if the first row can be read as a CSV line
                sample = csv_file.readline()
                if not sample:  # Empty file check
                    raise argparse.ArgumentTypeError(f"The file '{self.gcp_file}' is empty.")
                if self.separator not in sample:  # Delimiter check
                    raise argparse.ArgumentTypeError(f"The file '{self.gcp_file}' does not use {self.separator} as a separator.")
        except UnicodeDecodeError:
            print(f"The file '{self.gcp_file}' is not a valid UTF-8 encoded CSV file.")
            sys.exit()
        except Exception as e:
            print(f"Error reading {self.gcp_file}: {e}")
            sys.exit()



        while retry:
            try:
                self.gcps = pd.read_csv(self.gcp_file, sep=self.separator,
                                        skiprows=skiprows, header=None)
                retry = False
            except FileNotFoundError:
                messagebox.showerror("Error", f"File not found: {self.gcp_file}")
                return False
            except UnicodeDecodeError:
                messagebox.showerror("Error", f"Decode error: {self.gcp_file}")
                return False
            except pd.errors.ParserError:
                if retry:
                    skiprows = 1
                else:
                    messagebox.showerror("Error", f"File parse error: {self.gcp_file}")
                    return False
        if len(self.gcps.columns) == 4:
            self.gcps.columns = ["col", "row", "img", "id"]
        elif len(self.gcps.columns) == 5:
            self.gcps.columns = ["col", "row", "img", "id", "size"]
        elif len(self.gcps.columns) == 7:
            self.gcps.columns = ["east", "north", "elev", "col", "row", "img", "id"]
        else:
            messagebox.showerror("Error", f"Invalid number of columns: {self.gcp_file}")
            return False
        self.imgs = sorted(list(set(self.gcps["img"])))
        return True

    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        self.canvas.yview(*args, **kwargs)  # scroll vertically
        self.ShowImage()  # redraw the image

    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        self.canvas.xview(*args, **kwargs)  # scroll horizontally
        self.ShowImage()  # redraw the image

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.ShowImage()  # redraw the image

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        if not bbox[0] < x < bbox[2] or not bbox[1] < y < bbox[3]:
            return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 30:
                return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale /= self.delta
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale        *= self.delta
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.ShowImage()

    def ShowImage(self, event=None):
        """ show actual image with GCPs
        """
        if self.imgs is None or len(self.imgs) == 0:
            return
        name =self.imgs[self.img_no]
        if self.title() != name:    # new image to display
            self.title(name)   # show image name in title
            if path.exists(name):
                img_path = name
            if not path.exists(name):
                img_path = path.join(self.img_path, name)
            if not path.exists(img_path):
                img_path = path.join(path.split(self.gcp_file)[0], name)

            # load image

            if 'dng' in img_path.lower():
                dng = DngFile.read(img_path)
                self.image = Image.fromarray(dng.postprocess())  # demosaicing by rawpy
            else :
                self.image = PIL.Image.open(img_path)

            self.width, self.height = self.image.size

            # mark GCPs
            img = PIL.ImageDraw.Draw(self.image)
            for index, rec in self.gcps.loc[self.gcps['img'] == name].iterrows():
                x = rec["col"]
                y = rec["row"]
                shape = [(x - self.style["markersize"]/2, y - self.style["markersize"]/2),
                         (x + self.style["markersize"]/2, y + self.style["markersize"]/2)]
                img.ellipse(shape, outline=self.style["edgecolor"], width=self.style["edgewidth"])
                img.text((x + self.style["markersize"]/2, y + self.style["markersize"]/2),
                         str(rec["id"]), font=self.font, fill=self.style["fontcolor"],
                         stroke_width=20)
            self.container = self.canvas.create_rectangle(0, 0, self.width/5, self.height/5, width=0)
            self.imscale = 0.2

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(canvas_width),
                 self.canvas.canvasy(canvas_height))

        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]

        if bbox[0] == bbox2[0] and bbox[2] == bbox2[2]:  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if bbox[1] == bbox2[1] and bbox[3] == bbox2[3]:  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]

        self.canvas.configure(scrollregion=bbox)  # set scroll region
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]

        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
            image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = PIL.ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]),
                                               anchor='nw', image=imagetk)
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

        #canvas.scale(tk.ALL, x, y, xfactor, factor)    TODO zoom extent

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

    def back(self):
        self.img_no -= 1
        if self.img_no < 0:
            self.img_no = len(self.imgs) - 1
        self.ShowImage()

    def forward(self):
        self.img_no += 1
        if self.img_no >= len(self.imgs):
            self.img_no = 0
        self.ShowImage()

def cmd_params(parser):
    """ handle command line parameters

        :param parser: command line parser
    """
    def_separator = " "             # default separator is space
    def_markersize = 200            # marker size
    def_edgecolor = "red"           # edge color for markers
    def_edgewidth = 20              # edge width for markers
    def_fontsize = 200              # text height pixel
    def_fontcolor = 'red'           # inner color for GP ID annotation

    parser.add_argument('gcp_file_name', metavar='file_name', type=str, nargs='?',
                        help='GCP file to process')
    parser.add_argument('--command', type=str, default='all',
                        help='command all/ID show all images/images with GCP ID')
    parser.add_argument('--path', type=str, default='./',
                        help='input path for images')
    parser.add_argument('-s', '--separator', type=str, default=def_separator,
                        help=f'input file separator, default {def_separator}')

    # parameters for marker display
    parser.add_argument('--markersize', type=int, default=def_markersize,
                        help=f'marker size on image, default {def_markersize}')
    parser.add_argument('--edgecolor', type=str, default=def_edgecolor,
                        help=f'marker edge color, default {def_edgecolor}')
    parser.add_argument('--edgewidth', type=int, default=def_edgewidth,
                        help=f'marker edge width, default {def_edgewidth}')
    parser.add_argument('--fontsize', type=int, default=def_fontsize,
                        help=f'font size on image, default {def_fontsize}')
    parser.add_argument('--fontcolor', type=str, default=def_fontcolor,
                        help=f'font color on image, default {def_fontcolor}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    cmd_params(parser)
    args = parser.parse_args()
    if args.gcp_file_name:
        gcp_file_name = args.gcp_file_name
    else:
        gcp_file_name = None
    style = {'markersize': args.markersize,
             'edgecolor': args.edgecolor,
             'edgewidth': args.edgewidth,
             'fontsize': args.fontsize,
             'fontcolor': args.fontcolor,
            }

    # app = Tk()
    # width = int(app.winfo_screenwidth()/2)
    # height = int(app.winfo_screenheight()/2)
    # print(f'{width=} {height=}')
    # app.quit()
    width = 1024
    height = 768
    gcp_c = GcpCheck(style, gcp_file_name, args.separator,width=width,height=height ,img_path=args.path)
    gcp_c.mainloop()
    #if args.command == "all":
    #    gcp_c.ShowAll()
    #elif re.match("^[0-9]+$", args.command):
    #    gcp_c.ShowId(int(args.command))
    #else:
    #    gcp_c.ShowImage(args.command)
