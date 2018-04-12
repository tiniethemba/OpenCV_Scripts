import argparse
import cv2

class MyArgs():
    def __init__(self):
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--cam")
        ap.add_argument("-i", "--im")
        ap.add_argument("-vv","--vid")
        self.args = vars(ap.parse_args())

    def imcam(self):
        if self.args.get("im", 0):
            self.my_image = self.args["im"]
            lst = ["im", self.my_image]
            return lst
        elif self.args.get("cam", 0):
            self.cam_index = int(self.args["cam"])
            lst = ["cam", self.cam_index]
            return lst
        elif self.args.get("vid", 0):
            self.vid = self.args["vid"]
            lst = ["vid", self.vid]
            return lst
        else:
            return [0]

