import numpy as np
import cv2
from PIL import ImageChops

cap = cv2.VideoCapture(1)

ret1, frame1 = cap.read()
frame1 = cv2.resize(frame1,(360,240))
hsv_frame1 =cv2.cvtColor(frame1,cv2.COLOR_BGR2HSV)
while(1):
    ret, frame = cap.read()
    #hsv_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    #frame = cv2.resize(frame,(360,240))
    #hsv_frame = cv2.resize(hsv_frame, (360, 240))
    diff = ImageChops.difference(frame1, frame)
    #fgmask = fgbg.apply(frame)
    #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    #fgmask = cv2.subtract(hsv_frame1, hsv_frame)
    #fgmask = cv2.cvtColor(fgmask,cv2.COLOR_HSV2BGR)
    #res = cv2.bitwise_and(fgmask, frame1)
    cv2.imshow('frame',frame)
    cv2.imshow("result", diff)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

def denoise(frame):
    frame = cv2.medianBlur(frame, 5)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    return frame

cap.release()
cv2.destroyAllWindows()