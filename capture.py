###############################################################################
# RVIP STEREOBOOTH
###############################################################################

import cv2.cv as cv
import cv2
import numpy as np
import time
import os

from subprocess import call

# open the cameras
cams = [cv2.VideoCapture(), cv2.VideoCapture()] 
cams[0].open(1)
cams[1].open(2)

# Do our cameras need to be rotated? 
def transform(img):
    out = np.fliplr(np.rot90(img,-1))
    return out

# A named window is required for imshow() to work correctly
cv2.namedWindow("preview", cv.CV_WINDOW_NORMAL)
zoom=2
previewImageX=200*zoom
previewImageY=300*zoom

# This preview screen is intended for CALIBRATION
def preview(images):
    # scale the images down for display, and show them side by side
    # display a reticle over the images to help with convergence
    count = len(images)
    out = np.zeros((previewImageY, previewImageX*count, 3), dtype=np.uint8)
    i = 0
    for img in images:
        scaled = cv2.resize(img, (previewImageX, previewImageY))
        x = (previewImageX*i)
        out[0:previewImageY,x:x+previewImageX]=scaled
        cx = x + previewImageX/2
        cv2.line(out, (cx, 0), (cx, previewImageY), cv.RGB(200,200,200), 1)
        i+=1
    cv2.line(out, (0, previewImageY/2), (previewImageX*count, previewImageY/2),
             cv.RGB(200,200,200), 1)
    cv2.imshow('preview', out)

def grabAll():
    # is there a way to go faster?
    for cam in cams:
        cam.grab()

def captureAll():
    grabAll()	# fast thing we can do
    # this should be a map or something... 
    images = [cams[0].retrieve()[1], cams[1].retrieve()[1]]
    # transform images as nesc
    return map(transform, images)
    
def repeat():
    images = captureAll()
    preview(images)
    return images

def save(images, dir=False):
    print "Saving"
    dirstr = ""
    if(dir):
        os.mkdir(dir)
        dirstr = "%s/" % (dir)
    x = 0
    for img in images:
        cv2.imwrite("%simg-%s.png"%(dirstr, x), img)
        x+=1

def convert(name = "output.gif",delay=15, dir=False):
    # use convert from imagemagick to make an animated gif
    # convert -delay 20 -loop 0 img-*.png output.gif
    # full res:
    # call(["convert", "-delay", str(delay), "-loop", "0", "img-*.png", name])
    # Posterize
    cwd = os.getcwd()
    if(dir):
        os.chdir(dir)
    call(["convert", "-delay", str(delay), "-loop", "0",
          "-posterize","16",
          "-resize","50%",
          "img-*.png", name])
    if(dir):
        os.chdir(cwd)

def click():
    os.system("say click")

def bye():
    os.system("say bye")

def mainloop():
    # just wait for a key press, ESC, escapes
    k = -1
    while k!=27:	
        images = repeat()
        if k!=-1:
            images = repeat()
            click()
            dir = str(int(time.time()))	# number of seconds since epoch
            save(images,dir)
            convert(dir=dir)
        k = cv2.waitKey(1)	# -1 if nothing pressed
    bye()

if __name__ == "__main__":
    mainloop()
