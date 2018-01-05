import cv2
import numpy as np
try:
    cap = cv2.VideoCapture(0)
except TypeError:
    cap1 = cv2.VideoCapture(1)
    r1, f1 = cap1.read()
r,f = cap.read()


red = np.uint8([[[255,0,0 ]]])
green = np.uint8([[[0,255,0 ]]])
blue = np.uint8([[[0,0,255 ]]])

try:
    while(1):

        # Take each frame
        _, frame = cap.read(cv2.IMREAD_COLOR)
        _, frame2 = cap1.read(cv2.IMREAD_COLOR)

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #hsv_green = cv2.cvtColor(frame, green)
        # define range of blue color in HSV
        lower_blue = np.array([110,0,0])
        upper_blue = np.array([130,255,255])


        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask = mask)

        cv2.imshow('frame', frame)
        cv2.imshow('frame2', frame2)
        cv2.imshow("mask", mask)
        #cv2.imshow('mask',mask)
        #cv2.imshow('res',res)
        k = cv2.waitKey(5) & 0xFF
        print k
        # If the pressed button was the ESC button, except the loop
        if k == 27:
            break
except KeyboardInterrupt:
    raise SystemExit