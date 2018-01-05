import cv2
import numpy as np

cap = cv2.VideoCapture(0)


def denoise(frame):
    frame = cv2.medianBlur(frame, 5)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    return frame

while(1):

    # Take each frame
    _, frame = cap.read()

    frame = denoise(frame)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_blue = np.array([110,50,50])
    lower_blue1 = np.uint8([[[110,50,50]]])
    lower_blue_bgr = cv2.cvtColor(lower_blue1, cv2.COLOR_HSV2BGR)
    upper_blue = np.array([130,255,255])
    upper_blue1 = np.uint8([[[130, 255, 255]]])
    upper_blue_bgr = cv2.cvtColor(upper_blue1, cv2.COLOR_HSV2BGR)

    print lower_blue_bgr
    print upper_blue_bgr


    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    #mask_red

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
