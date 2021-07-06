# -*- coding: utf-8 -*-
"""
Created on Tue Jul  6 17:27:05 2021

@author: 123
"""
import cv2

src = cv2.imread(".\\sample2.png")
dst = src.copy()

gray = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)
ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

for i in contours:
    M = cv2.moments(i)
    try:
        cX = int(M['m10'] / M['m00'])
        cY = int(M['m01'] / M['m00'])
        cv2.circle(dst, (cX,cY), 3, (255, 0 , 0) , -1)
        cv2.drawContours(dst, [i], 0, (0, 0, 255), 2)
    except ZeroDivisionError:
        print('zero division')
        
  
cv2.imshow("dst", dst)
cv2.waitKey()
cv2.destroyAllWindows()