import numpy as np
import cv2
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--cam")
ap.add_argument("-i", "--im")
args = vars(ap.parse_args())


class getHSV():
    def __init__(self):
        # Creating a window for later use
        cv2.namedWindow('result')

        # Starting with 100's to prevent error while masking
        self.h, self.s, self.v = 100, 100, 100
        cv2.createTrackbar('h', 'result', 0, 179, self.nothing)
        cv2.createTrackbar('s', 'result', 0, 255, self.nothing)
        cv2.createTrackbar('v', 'result', 0, 255, self.nothing)
        if args.get("im", 0):
            self.my_image = args["im"]
        else:
            self.cam_index = int(args["cam"])
            self.cap = cv2.VideoCapture(self.cam_index)

    def filter(self):


        while (True):
            if args.get("im", 0):
                frame = cv2.imread(self.my_image)
            else:
                _, frame = self.cap.read()

            frame = cv2.resize(frame, (480, 360))
            frame = self.denoise(frame)

            # converting to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # get info from track bar and appy to result
            self.h = cv2.getTrackbarPos('h', 'result')
            self.s = cv2.getTrackbarPos('s', 'result')
            self.v = cv2.getTrackbarPos('v', 'result')

            # Normal masking algorithm
            lower = np.array([self.h, self.s, self.v])
            upper = np.array([255, 255, 255])

            self.mask = cv2.inRange(hsv, lower, upper)

            self.result = cv2.bitwise_and(frame, frame, mask=self.mask)
            cv2.imshow('result', self.result)

            self.k = cv2.waitKey(5) & 0xFF
            if self.k == 27:
                break

        # When everything done, release the capture
        self.cap.release()
        cv2.destroyAllWindows()

    def denoise(self,frame):
        frame = cv2.medianBlur(frame, 5)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        return frame

    def nothing(self):
        pass





