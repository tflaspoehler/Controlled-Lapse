# ---------------------
# GUI-related libraries 
from  Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
# -----------------
# better fonts
import ttk, tkFont
# -----------------------
# python image library
from PIL import Image, ImageTk, ImageDraw, ExifTags
# -----------------------
# basic pythong libraries
from math import *
import os, sys, time, unicodedata, operator
# -----------------------

# ===================
#   image bar class
# ===================
class image_bar_class(Frame):
    def __init__(self, images, parent, root):
        ###self.parent = parentself.fig = plt.figure()
        self.root = root
        self.parent = parent
        self.images = images
        self.line = None
        self.zoom = 10.0
        self.draw(images)
        
    def draw(self, images):
        Frame.__init__(self, self.parent, bg='black')
        
        self.reel = Canvas(self, width=int(float(self.root.winfo_width())), height=self.parent.winfo_height())
        self.scroll = Scrollbar(self, orient=HORIZONTAL, command=self.reel.xview)
                
        self.reel.configure(xscrollcommand=self.scroll.set)
        self.reel.configure(scrollregion=(0, 0, int(float(self.root.winfo_width())*self.zoom), self.parent.winfo_height()))
        
        self.scroll.pack(fill=BOTH, expand=TRUE)
        self.reel.pack(fill=Y, expand=TRUE)
        
        self.roll = Frame(self.reel, bg='black')
        self.roll.pack(fill=BOTH, expand=TRUE)
        self.reel.create_window((0, 0), window=self.roll, anchor="nw", tags="self.roll")
        height = self.parent.winfo_height() - 17
        width = self.parent.winfo_width()
        self.window_width = width
        img = Image.open(images[0].filename)
        image_width  = img.width * height / img.height
        n = int(ceil(self.zoom * float(width) / float(image_width)))
        column = 1
        self.labels = []
        self.image_canvas = []
        for i in range(0, len(images), len(images)/n):
            img = Image.open(images[i].filename)
            img = img.resize((img.width * height / img.height, height), Image.ANTIALIAS)
            self.image_canvas.append(ImageTk.PhotoImage(img))
            self.labels.append(Label(self.roll, image=self.image_canvas[-1], 
                                ## text=repr(images[i].id),
                                borderwidth=0,
                                compound="center",
                                highlightthickness = 0,
                                padx=0,
                                pady=0,
                                bg='black'))
            self.labels[-1].grid(row=0, column=column)
            self.labels[-1].bind('<Button-1>', self.click)
            self.labels[-1].bind('<B1-Motion>', self.click)
            self.labels[-1].bind('<B3-Motion>', self.wheel)
            column += 1
        
    def click(self, event):
        x = self.parent.winfo_pointerx() - self.parent.winfo_rootx()
        percent = float(len(self.images))*self.reel.canvasx(x)/(float(self.root.winfo_width())*self.zoom)
        if (percent > len(self.images)):
            percent = len(self.images)
        elif (percent < 1):
            percent = 1
        self.root.show_image(self.images[int(percent)-1])
        self.root.update_idletasks()
        
    def wheel(self, event):
        print self.zoom, event.delta
        self.zoom = self.zoom * event.delta
        self.reel.xview_moveto(-100.0)
        print self.zoom
# -------------------