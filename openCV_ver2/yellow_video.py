import cv2 as cv
import numpy as np
import imutils
from shapedetector import ShapeDetector

cap = cv.VideoCapture(1)


while (True):
    image = cv.imread('http://192.168.66.1:9527/videostream.cgi?loginuse=admin&loginpas=admin')
    ret, image = cap.read()
    height, width = image.shape[:2]
    image = cv.resize(image, (width, height), interpolation=cv.INTER_AREA)

    # draw rectangles
    image = cv.rectangle(image, (560, 160), (640, 320), (255, 0, 0) , 1, cv.LINE_4)
    image = cv.rectangle(image, (0, 160), (80, 320), (255, 0, 0), 1, cv.LINE_4)

    #track circle object
    resized = imutils.resize(image, width=300)
    ratio = image.shape[0] / float(resized.shape[0])

    print(ratio)

    cv.imshow("image", image)
    if cv.waitKey(1) & 0xFF == 27:
        break

    """
    gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
       r2, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)
       binary = cv.bitwise_not(binary)

       contours, hierarchy = cv.findContours(binary, cv.RETR_CCOMP, cv.CHAIN_APPROX_NONE)

       for i in range(len(contours)):
           cv.drawContours(image, [contours[i]], 0, (255, 0, 0), 1)
           #cv.putText(image, str(i), tuple(contours[i][0][0]), cv.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 1)




       b,g,r = cv.split(image)

       ret, dst = cv.threshold(g, 190, 255, cv.THRESH_BINARY)

       r2, d2 = cv.threshold()

       cv.imshow("dst", dst)

       """

cv.destroyAllWindows()
