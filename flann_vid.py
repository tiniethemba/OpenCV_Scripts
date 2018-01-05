import numpy as np
import cv2
from matplotlib import pyplot as plt
import time

MIN_MATCH_COUNT = 10
img1 = cv2.imread('bnr1.jpg',0)
img1 = cv2.resize(img1, (0,0), fx=0.5, fy=0.5)
cap = cv2.VideoCapture(0)
r1,f1 = cap.read()
firsttime = True
sift = cv2.xfeatures2d.SIFT_create()
kp1, des1 = sift.detectAndCompute(img1,None)
while True:
    time.sleep(0.1)
    r,f = cap.read()
    f = cv2.resize(f, (0, 0), fx=0.5, fy=0.5)
    f = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)

    kp2, des2 = sift.detectAndCompute(f,None)
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,np.load(des2),k=2)

    # store all the good matches in good list as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    if firsttime == True:
        h1, w1 = f.shape[:2]
        h2, w2 = img1.shape[:2]
        nWidth = w1 + w2
        nHeight = max(h1, h2)
        hdif = (h1 - h2) / 2
        firsttime = False

    result = np.zeros((nHeight, nWidth,3), np.uint8)
    result[hdif:hdif + h2, :w2] = img1
    result[:h1, w2:w1 + w2] = f
    print len(matches)
    if len(matches) > 0:
        for i in range(len(matches)):
            pt_a = (int(kp1[matches[i].trainIdx].pt[0]), int(kp1[matches[i].trainIdx].pt[1] + hdif))
            pt_b = (int(kp2[matches[i].queryIdx].pt[0] + w2), int(kp2[matches[i].queryIdx].pt[1]))
            cv2.line(result, pt_a, pt_b, (0, 150, 255), thickness=2)

    cv2.imshow('Camera', result)
    # draw matches in yellow color
    draw_params = dict(matchColor = (0,255,255), singlePointColor = None, # draw only inliers
    flags = 2)

    img3 = cv2.drawMatches(img1,kp1,f,kp2,good,None,**draw_params)
    cv2.imshow("flannpic.jpg", img3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
