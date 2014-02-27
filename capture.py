###############################################################################
# RVIP STEREOBOOTH
###############################################################################

import cv2.cv as cv
import cv2
import numpy as np
import base62
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
        dir = "images/%s" % (dir)
        os.mkdir(dir)
        dirstr = "%s/" % (dir)
    x = 0
    for img in images:
        cv2.imwrite("%simg-%s.png"%(dirstr, x), img)
        x+=1

#
# use scp to copy the resulting gif to rvip.co, for example:
# scp -i ~/.ssh/scottaws.pem ./cat.gif
#     ubuntu@ec2-107-22-117-177.compute-1.amazonaws.com:/home/ubuntu/sites/rvip/photos
#
# If this fails - which it may due to network suckery, we rely on a seperate rsync process
# to move the images over
#
def cp(dir=False):
    print "Copying %s/output.gif to rvip.co" % (dir)
    if(dir):
        src = "images/%s/%s.gif" % (dir,dir)
        remotedst = "/home/ubuntu/sites/rvip/photos/%s.gif" % (dir)
        localdst = "images/photos/%s.gif" % (dir)
        call(["cp", src, localdst])
        result = call(["scp","-i", "rvip.co.pem",
                       src,
                       "ubuntu@ec2-107-22-117-177.compute-1.amazonaws.com:%s" % (remotedst)])
        return result==0
    return False

def convert(name,delay=15, dir=False):
    # use convert from imagemagick to make an animated gif
    # convert -delay 20 -loop 0 img-*.png output.gif
    # full res:
    # call(["convert", "-delay", str(delay), "-loop", "0", "img-*.png", name])
    # Posterize
    cwd = os.getcwd()
    print "CHDIR = "+dir
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

button=False
saveAs=False

def mainloop():
    global button
    # just wait for a key press, ESC, escapes
    k = -1
    while k!=27:	
        images = repeat()
        if k!=-1 or button:
            images = repeat()
            click()
            name = saveAs
            if(not name):
                # generate a short code based on time
                name = str(base62.encode(int(time.time())-1392050000))
            save(images,name)
            convert(name+".gif", dir="images/%s"%(name) )
            cp(name)                     # TRY and copy the file to rvip.co
            button = False
        k = cv2.waitKey(1)	# -1 if nothing pressed
    bye()

###############################################################################
## make a button we can hit from the web to take a picture
###############################################################################

from bottle import route, run, template, static_file

@route('/click')
@route('/click/<filename>')
def index(filename=False):
    global button, saveAs
    oldbutton = button
    saveAs = filename
    button = True
    return "button was %s now %s" % (oldbutton, button)

@route('/static/<filename>')
def server_static (filename):
    """ serve up static files and assets """
    return static_file(filename, root="./static")

import thread
thread.start_new_thread(lambda: run(host='localhost', port=8000), ())


###############################################################################

if __name__ == "__main__":
    mainloop()
