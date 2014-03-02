import cv2
import cv2.cv as cv
import numpy as np

cv2.namedWindow("out",cv.CV_WINDOW_NORMAL)
i1 = cv2.imread("img-0.png")
i2 = cv2.imread("img-1.png")

o1 = cv2.resize(i1, (480,640))
o2 = cv2.resize(i2, (480,640))

# rotate
def rotateImage(image, angle):
    center=tuple(np.array(image.shape[0:2])/2)
    rot_mat = cv2.getRotationMatrix2D(center,angle,1.0)
    return cv2.warpAffine(image, rot_mat, image.shape[0:2],flags=cv2.INTER_LINEAR)

cv2.imshow("out", rotateImage(o1, 11))

