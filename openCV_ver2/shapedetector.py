# -*- coding: utf-8 -*-
import cv2

class ShapeDetector:
    def _init_(self):
        pass
    
    def detect(self, c):
        #initialize the shape name and approximate the contour
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        
        if len(approx) == 3:
            shape = "triangle"
            
        elif len(approx) == 4:
            
            (x,y,w,h) = cv2.boundingRect(approx)
            ar = w / float(h)
            
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
            
        elif len(approx) == 5:
            shape = "pentagon"
            
        else:
            shape = "circle"
            
        return shape