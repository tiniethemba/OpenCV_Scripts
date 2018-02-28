import cv2
import numpy as np

class ColourFilter():
    def __init__(self, frame, lower, upper):
        self.frame = frame
        self.HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        self.lower = lower
        self.upper = upper


    def filt(self):
        self.mask = cv2.inRange(self.HSV, self.lower, self.upper)
        return self.mask
