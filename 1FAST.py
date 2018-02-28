import numpy as np
import cv2
# 1FAST.py draws keypoints for matching using th FAST algorithm
cap = cv2.VideoCapture(0)
#cap1 = cv2.VideoCapture(1)
r,f = cap.read()

while(cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Initiate FAST object with default values
    fast = cv2.FastFeatureDetector_create(threshold=7)
    kp = fast.detect(frame,None)
    #kp1 = fast1.detect(frame1, None)

    #frame = cv2.drawKeypoints(frame, kp, color=(0,255,255),outImage=0,flags = 0)
    #frame1 =  cv2.drawKeypoints(frame1, kp1, color=(0,255,255),outImage=0,flags = 0)
    # Print all default params
    print "Threshold: ", fast.getThreshold()
    print "nonmaxSuppression: ", fast.getNonmaxSuppression()
    print "neighborhood: ", fast.getType()
    print "Total Keypoints with nonmaxSuppression: ", len(kp)
    frame = cv2.resize(frame, (640,480))
    cv2.imshow('Computer WebCam',frame)
    # Create black (zeroed pixels) image, the same size as the frame
    mask = np.zeros((frame.shape[0],frame.shape[1], 3), np.uint8)
    mask[:] = (0,0,0)

    # Draw the kp's in yellow over the black image
    fmask = cv2.drawKeypoints(mask, kp, None, color=(255, 0, 0), flags=0)
    frame1 = cv2.drawKeypoints(frame,kp,None,color= (0,0,0), flags=0)
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    __,cons ,_= cv2.findContours(frame1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    print "CONS",len(cons)
    for i in range(len(cons)):
        x, y, w, h = cv2.boundingRect(cons[i])
        cv2.rectangle(frame1,(x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow('Keypoints only', fmask)
    cv2.imshow("BLOW", frame1)

    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()