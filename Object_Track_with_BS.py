import numpy as np
import cv2
from collections import deque

from operator import itemgetter


class BackGroundSubtractor:
    # When constructing background subtractor, we
    # take in two arguments:
    # 1) alpha: The background learning factor, its value should
    # be between 0 and 1. The higher the value, the more quickly
    # your algorithm learns the changes in the background. Therefore,
    # for a static background use a lower value, like 0.001. But if
    # your background has moving trees and stuff, use a higher value,
    # maybe start with 0.01.
    # 2) firstFrame: This is the first frame from the video/webcam.
    def __init__(self, alpha, firstFrame):
        self.alpha = alpha
        self.backGroundModel = firstFrame
        self.lockModel = False

    def getForeground(self, frame, threshold=(20, 255)):
        mask = self.getMask(frame, threshold)

        fg = cv2.bitwise_and(frame, frame, mask=mask)

        return fg

    def lockBG(self):
        self.lockModel = True

    def lockBG(self):
        self.lockModel = False

    def getMask(self, frame, threshold):
        # Learn the new frame only if the model is not locked
        if self.lockModel is False:
            # apply the background averaging formula:
            # NEW_BACKGROUND = CURRENT_FRAME * ALPHA + OLD_BACKGROUND * (1 - APLHA)
            self.backGroundModel = frame * self.alpha + self.backGroundModel * (1 - self.alpha)

        # after the previous operation, the dtype of
        # self.backGroundModel will be changed to a float type
        # therefore we do not pass it to cv2.absdiff directly,
        # instead we acquire a copy of it in the uint8 dtype
        # and pass that to absdiff.

        maskRGB = cv2.absdiff(self.backGroundModel.astype(np.uint8), frame)

        mask = cv2.cvtColor(maskRGB, cv2.COLOR_BGR2GRAY)

        # Apply thresholding on the background and display the resulting mask
        _, mask = cv2.threshold(mask, threshold[0], threshold[1], cv2.THRESH_BINARY)

        return mask

    def getModel(self):
        return self.backGroundModel.astype(np.uint8)


class ROI:
    def __init__(self, track_window):
        x = track_window[0]
        y = track_window[1]

        width = track_window[2]
        height = track_window[3]

        self.start = (x, y)
        self.end = (x + width, y + height)

    def drawBoundary(self, frame):
        cv2.rectangle(frame, self.start, self.end, (0, 255, 0), 1)

    def getROI(self, frame):
        return frame[self.start[1]:self.end[1], self.start[0]:self.end[0]]


def denoise(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)

    frame = cv2.medianBlur(frame, 5)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)

    # r,g,b = cv2.split(frame)

    # r = cv2.equalizeHist(r)

    # g = cv2.equalizeHist(g)

    # b = cv2.equalizeHist(b)

    # frame = cv2.merge((r,g,b))

    return frame


def findCenter(frame):
    # Calculate the co-ordinates for the center pixel
    y = frame.shape[0] / 2
    x = frame.shape[1] / 2

    return (x, y)


def getObject(frame, hsv):
    lower = np.array([0, 0, 0], dtype=np.uint8)
    upper = np.array([0, 0, 0], dtype=np.uint8)

    lower[0] = hsv[0] - 5
    # lower[1] = hsv[1]-10
    lower[1] = 0
    lower[2] = hsv[2] - 40

    upper[0] = hsv[0] + 5
    # upper[1] = hsv[1]+40
    upper[1] = 255
    upper[2] = hsv[2] + 40

    return cv2.inRange(frame, lower, upper)


INK = None
pts = None


def drawLines(obj, frame):
    global INK
    global pts
    if (INK == None):
        INK = np.zeros([frame.shape[0], frame.shape[1]], dtype=np.uint8)

    if (pts == None):
        pts = deque(maxlen=100000)

    _, contours, _ = cv2.findContours(obj, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Nothing to do, if no contours were found
    if (len(contours) == 0):
        return

    # get all areas and indexes
    contourAreas = [(index, cv2.contourArea(cnt)) for index, cnt in enumerate(contours)]

    # select the index having the greatest contour area.
    ci = max(contourAreas, key=itemgetter(1))[0]

    cnt = contours[ci]

    x, y, w, h = cv2.boundingRect(cnt)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 1)

    if len(contours) > 0:
        center = (x + (h / 2), y + (w / 2))

        # update the points queue
        if (LOCKED is True and DRAW_PRESSED is True):
            pts.appendleft(center)



            # loop over the set of tracked points
    for i in xrange(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line andq
        # draw the connecting lines
        # thickness = float(np.sqrt(100000 / float(i + 1)) * 2.5)
        if (LOCKED is True):
            cv2.line(INK, pts[i - 1], pts[i], (255), 2)

            # if(INK != None):
            # 	cv2.imshow('INK',cv2.flip(INK,1))


def getMedian(roi):
    h, s, v = cv2.split(roi)

    medianH = np.median(h)
    medianS = np.median(s)
    medianV = np.median(v)

    return (medianH, medianS, medianV)


##################################################################################################

DRAW_PRESSED = True
LOCKED = False
center = (0, 0)
HSV = (0, 0, 0)
# x, y, width, height
trackWindow = (0, 0, 0, 0)

reigon1 = ROI(trackWindow)

cam = cv2.VideoCapture(1)

ret, frame = cam.read()
if ret is True:
    center = findCenter(frame)
    trackWindow = (center[1], center[0], 15, 15)
    reigon1 = ROI(trackWindow)
    backSubtractor = BackGroundSubtractor(0.01, denoise(frame))
    backSubtractor.lockModel = True
    run = True
else:
    run = False

while (run):
    # Read a frame from the camera
    ret, fr = cam.read()

    frame = denoise(fr.copy())

    # If the frame was properly read.
    if ret is True:

        # get the foreground
        fg = backSubtractor.getForeground(frame, (25, 255))

        # convert to hsv
        # fgHSV = cv2.cvtColor(fg,cv2.COLOR_BGR2HLS)
        # fgHSV = fg

        if not LOCKED:
            # Convert the frame to HSV
            # frameHSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HLS)
            # Calculate the mean HSV of ROI
            # HSV = cv2.mean(reigon1.getROI(frameHSV))
            HSV = getMedian(reigon1.getROI(frame))

            reigon1.drawBoundary(fr)

        obj = getObject(fg, HSV)

        obj = cv2.erode(obj, np.ones((5, 5), np.uint8), iterations=1)

        disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        cv2.filter2D(obj, -1, disc, obj)

        fg = backSubtractor.getForeground(frame)
        if (INK.all() == None):
            INK = np.zeros([frame.shape[0], frame.shape[1]], dtype=np.uint8)
        drawLines(obj.copy(), fr)

        global INK
        if INK.all() != None:
            fr[:, :, 2] = cv2.bitwise_or(INK, fr[:, :, 2])

        cv2.imshow('object', cv2.flip(obj, 1))

        cv2.imshow('frame', cv2.flip(fr, 1))

        cv2.imshow('foreground', cv2.flip(fg, 1))

        key = cv2.waitKey(1) & 0xFF

        if key == 27:
            break
        elif key == ord('l'):
            LOCKED = True
            backSubtractor = BackGroundSubtractor(0.01, frame)
        elif key == ord('u'):
            LOCKED = False

        elif key == ord('b'):
            # Toggle background averaging state
            backSubtractor.lockModel = not backSubtractor.lockModel
            if backSubtractor.lockModel is True:
                print 'BG locked'
            else:
                print 'BG unlocked'

        elif key == ord('c'):
            pts = deque(maxlen=100000)
            INK = None

        if key == ord('d'):
            DRAW_PRESSED = True
        else:
            DRAW_PRESSED = False
            pts = None




    else:
        break

cam.release()
cv2.destroyAllWindows()