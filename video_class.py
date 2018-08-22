# ---------------------
# GUI-related libraries 
from  Tkinter import *
# -----------------------
# python image library
from PIL import Image, ImageTk, ImageDraw, ExifTags
# -----------------------
# all command line stuff
import os, sys, subprocess, tempfile
# -----------------------

# ===================
#    video class
# ===================

class video_class(Frame):
    def __init__(self, id, name, files, parent, root, active, rate=200):
        self.id = id
        self.name = name
        self.parent = parent
        self.files = files
        self.root = root
        self.active = active
        self.rate = rate
        self.draw()
        
    def draw(self):
        self.bg = 'black'
        if self.active:
            self.bg = '#035'
        print 'video class files', len(self.files)
        img = Image.open(self.files[len(self.files)/2].filename)
        self.image = ImageTk.PhotoImage(img.resize((100, img.height * (100) / img.width), Image.ANTIALIAS))
        self.label = Label(self.parent, image=self.image,
                            borderwidth=0,
                            compound="center",
                            highlightthickness = 0,
                            width=100+10,
                            height=10 + (img.height * (100) / img.width),
                            bg=self.bg)
        self.label.bind('<ButtonPress-1>', self.click)
        self.label.bind('<Enter>', self.enter)
        self.label.bind('<Leave>', self.leave)
        self.label.pack(fill=X)
        
        self.name_var = StringVar()
        self.name_var.set(self.name)
        self.name_var.trace("w", self.name_call)
        self.name_entry = Entry(self.parent, textvariable=self.name_var, bg=self.bg, fg='white', borderwidth=0, justify=CENTER)
        self.name_entry.pack()
        self.name_entry.focus_force()
        
        self.scale = Scale(self.parent, from_=1, to=500, orient=HORIZONTAL, bg=self.bg, fg='white', highlightthickness=0, borderwidth=0, troughcolor=self.bg, label='fps', command=self.frame_rate)
        self.scale.set(self.rate)
        self.scale.pack(fill=X)

    def name_call(self, *args):
        self.name = self.name_var.get()

    def frame_rate(self, *args):
        self.rate = self.scale.get()
        
    def click(self, event):
        self.root.select_video(self.id)
        
    def enter(self, event):
        if self.active:
            self.label.configure(bg='#35b')
        else:
            self.label.configure(bg='#999')
            
    def leave(self, event):
        self.label.configure(bg=self.bg)
        
    def make_video(self):
    
        rtndir = os.getcwd()
        tmpdir = tempfile.gettempdir()  + '\\test' + '\\video' + repr(self.id)
        
        command = ['rd', '/s', '/q', tmpdir]
        print 'rmdir command:      ', command
        try:
            bash = subprocess.check_output(command, shell=True)
            print bash
        except:
            pass
                        
        command = ['mkdir', tmpdir]
        print 'mkdir command:      ', command
        try:
            bash = subprocess.check_output(command, shell=True)
            print bash
        except:
            pass
       
        for i in range(1, len(self.files)+1):
            command = ['mklink', tmpdir  + '\\' + str(i) + '.jpg', self.files[i-1].directory.replace('/','\\') + '\\' + self.files[i-1].filename]
            try:
                bash = subprocess.check_output(command, shell=True)
                ## print bash
            except:
                pass
                
        command = 'ffmpeg'
        
        os.chdir(tmpdir)
        print 'changed directory to', tmpdir
        command = [command, '-r', repr(self.scale.get()),  '-start_number', '1', '-i', '%d.jpg', '-b', '8000k', '-vcodec', 'libx264', '-pix_fmt', 'yuv420p',  self.name.replace(' ','.') + '.avi']
        print 'ffmpeg command:      ', command
        
        try:
            bash = subprocess.check_output(command, shell=True)
            print bash
        except:
            pass
            
            
        command = ['copy', self.name.replace(' ','.') + '.avi', self.root.save_directory.replace('/','\\') + '\\' + self.name.replace(' ','.') + '.avi']
        print 'copy command:      ', command
        
        try:
            bash = subprocess.check_output(command, shell=True)
            print bash
        except:
            pass
        
            
        os.chdir(rtndir)
        ##bash = subprocess.Popen([command], shell=True)
# -----------------