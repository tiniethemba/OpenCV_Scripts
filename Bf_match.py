import cv2
import copy
import matplotlib.pyplot as plt
import numpy as np
import time

source = cv2.imread('calc1.jpg',0)
cap = cv2.VideoCapture(0)

############# ORB descriptor #####################
orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(source, None)


while True:
    ret, frame = cap.read()
    time.sleep(0.25)
    ########### feature extraction by using ORB ############
    origin = copy.copy(frame)
    kp2, des2 = orb.detectAndCompute(origin, None)

    ########### Brute Force Matching ############
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1,des2)             #### keeps raising error at here*

    sorted_matches = sorted(matches, key=lambda x: x.distance)

    ########### Result ###########
    image = cv2.drawMatches(source, kp1, frame, kp2, sorted_matches[:8], None, flags=2)
    cv2.imshow("origin", origin)
    if image is not None:
        cv2.imshow("img",image)
    #cv2.imshow('matching', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()