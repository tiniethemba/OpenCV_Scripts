import numpy as np
import cv2
import time

cap = cv2.VideoCapture(0)
#cap1 = cv2.VideoCapture(1)
trainIm = cv2.imread("bnr1.png",0)
orb1 = cv2.ORB_create()
initkp, initdes = orb1.detectAndCompute(trainIm, None)
r1,f1 = cap.read()
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640,480))
try:
    while(True):
        ret, frame1 = cap.read()
        time.sleep(0.15)
        #ret1,frame1 = cap1.read(cv2.IMREAD_COLOR)
        # Initiate orb object with default values
        orb = cv2.ORB_create()
        #orb1 = cv2.orbFeatureDetector_create(threshold=15)
        # find and draw the keypoints
        #cv2.orbFeatureDetector_create()
        kp, des = orb.detectAndCompute(frame1,None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(initdes, des)
        #matches = sorted(matches, key=lambda x: x.distance)
        # kp1 = orb1.detect(frame1, None)
        dist = [m.distance for m in matches]
        if len(dist) is not 0:
            thres_dist = (sum(dist) / len(dist)) *.5
            matches = [m for m in matches if m.distance < thres_dist]
        frame = cv2.drawKeypoints(frame1, kp, color=(0,255,255),outImage=0,flags = 0)
        #frame1 =  cv2.drawKeypoints(frame1, kp1, color=(0,255,255),outImage=0,flags = 0)
        # Print all default params
        print len(matches)
        cv2.imshow('Computer WebCam',frame1)
        #cv2.imshow("External Webcam", frame1)
        #out.write(frame1)
        if len(dist) is not 0:
            b = cv2.drawMatches(frame1,kp,trainIm,initkp,matches[:20],None, flags =2)
        cv2.imshow("Match", b)
        mask = np.zeros((frame.shape[0],frame.shape[1], 3), np.uint8)
        mask[:] = (0,0,0)
        fmask = cv2.drawKeypoints(mask, kp, None, color=(0, 255, 255), flags=0)
        #cv2.imshow('Keypoints only', fmask)
        k = cv2.waitKey(10) & 0xFF
        if k == 27:
            break
except KeyboardInterrupt:
    raise SystemExit