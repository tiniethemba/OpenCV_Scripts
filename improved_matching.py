import numpy as np
import cv2

# Matcher class compares the training photo to the webcam.


ESC = 27
camera = cv2.VideoCapture(0)
orb = cv2.ORB_create()
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

imgTrainColor = cv2.imread('pic4.jpg')
imgTrainGray = cv2.cvtColor(imgTrainColor, cv2.COLOR_BGR2GRAY)

pole = cv2.imread("cropped_pic.jpg")
pole = cv2.cvtColor(pole, cv2.COLOR_BGR2GRAY)

poleTrain = orb.detect(pole, None)
poleTrain, desPole = orb.compute(pole, poleTrain)

kpTrain = orb.detect(imgTrainGray, None)
kpTrain, desTrain = orb.compute(imgTrainGray, kpTrain)

firsttime = True

class Matcher():
    def __init__(self, firsttime, matches, threshold, kpCam, kpTrain, imgCam, imgTrain):
        self.firsttime = firsttime
        self.matches = matches # list of matches list
        self.thresh = threshold
        self.imgCamColor = imgCam
        self.imgTrainColor = imgTrain

    def main(self):

        if self.firsttime == True:
            h1, w1 = imgCamColor.shape[:2]
            h2, w2 = imgTrainColor.shape[:2]
            nWidth = w1 + w2
            nHeight = max(h1, h2)
            hdif = (h1 - h2) / 2
            self.firsttime = False
        for match in self.matches:
            dist = [m.distance for m in match]
            if len(dist) is not 0:
                thresh_dist = (sum(dist) / len(dist)) * self.thresh
                print"Before:", match
                print "Threshold distance: ", thresh_dist
            self.result = np.zeros((nHeight, nWidth, 3), np.uint8)
            self.result[hdif:hdif + h2, :w2] = imgTrainColor
            self.result[:h1, w2:w1 + w2] = imgCamColor
            print "Match list length:", len(match)

            if len(match) > 0:
                for i in range(len(match)):
                    pt_a = (int(kpTrain[match[i].trainIdx].pt[0]), int(kpTrain[match[i].trainIdx].pt[1] + hdif))
                    pt_b = (int(kpCam[match[i].queryIdx].pt[0] + w2), int(kpCam[match[i].queryIdx].pt[1]))
                    cv2.line(self.result, pt_a, pt_b, (0, 150, 255), thickness=2)

    def show(self):
        cv2.imshow('Camera', self.result)

while True:

    ret, imgCamColor = camera.read()
    imgCamGray = cv2.cvtColor(imgCamColor, cv2.COLOR_BGR2GRAY)
    kpCam = orb.detect(imgCamGray, None)
    kpCam, desCam = orb.compute(imgCamGray, kpCam)
    matches = bf.match(desCam, desTrain)
    matches2 = bf.match(desPole, desTrain)
    match_list =[matches, matches2]
    matcher = Matcher(firsttime, match_list, 0.2, kpCam, kpTrain, imgCamColor,imgTrainColor)
    matcher.main()
    matcher.show()
    key = cv2.waitKey(20)
    if key == ESC:
        break

cv2.destroyAllWindows()
camera.release()