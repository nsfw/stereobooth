###############################################################################
# RVIP STEREOBOOTH
###############################################################################

import cv2.cv as cv
import cv2
import time
import numpy as np

from subprocess import call

# open the cameras
cams = [cv2.VideoCapture(), cv2.VideoCapture()] 
cams[0].open(1)
cams[1].open(2)

# A named window is required for imshow() to work correctly
cv2.namedWindow("preview")
previewImageX=300
previewImageY=200

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


def configCam(cam):
    pass
    # cv.SetCaptureProperty(cam, cv.CV_CAP_PROP_FRAME_WIDTH, 800)
    # cv.SetCaptureProperty(cam, cv.CV_CAP_PROP_FRAME_HEIGHT, 600)

def config():
    for cam in cams:
        configCam(cam)

def grabAll():
    # is there a way to go faster?
    for cam in cams:
        cam.grab()

def captureAll():
    grabAll()	# fast thing we can do
    return [cams[0].retrieve()[1], cams[1].retrieve()[1]]

def repeat():
    images = captureAll()
    preview(images)
    return images

def save(images):
    print "Saving"
    print images
    x = 0
    for img in images:
        cv2.imwrite("img-%s.png"%(x), img)
        x+=1


def convert(name = "output.gif",delay=15):
    # use convert from imagemagick to make an animated gif
    # convert -delay 20 -loop 0 img-*.png output.gif
    # full res:
    # call(["convert", "-delay", str(delay), "-loop", "0", "img-*.png", name])
    # Posterize
    call(["convert", "-delay", str(delay), "-loop", "0",
          "-posterize","8",
          "-resize","50%",
          "img-*.png", name])

# def do(fx):
#     while cv.WaitKey(1000) == -1:
#         images=captureAll()
#         time.sleep(0.01)
#     save(images)
#     convert()

def do(fx):
    while cv.WaitKey(1) == -1:
        images = repeat()
        time.sleep(0.01)
    save(images)
    convert()

if __name__ == "__main__":
    do(repeat)
