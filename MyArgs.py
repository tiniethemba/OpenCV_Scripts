import argparse
import cv2

class MyArgs():
    def __init__(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--cam")
        ap.add_argument("-i", "--im")
        self.args = vars(ap.parse_args())

    def imcam(self):
        if self.args.get("im", 0):
            self.my_image = self.args["im"]
            lst = ["im", self.my_image]
            return lst
        elif self.args.get("cam", 0):
            self.cam_index = int(self.args["cam"])
            self.cap = cv2.VideoCapture(self.cam_index)
            lst = ["cam", self.cap]
            return lst
        else:
            return [0]

