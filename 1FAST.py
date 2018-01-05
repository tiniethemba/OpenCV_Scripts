import numpy as np
import cv2

cap = cv2.VideoCapture(0)
#cap1 = cv2.VideoCapture(1)
r,f = cap.read()
#r1,f1 = cap1.read()
#fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter("output.avi", fourcc, 20.0, (640,480))
try:
    while(cap.isOpened()):
        ret, frame = cap.read(cv2.IMREAD_COLOR)
        #ret1,frame1 = cap1.read(cv2.IMREAD_COLOR)
        # Initiate FAST object with default values
        fast = cv2.FastFeatureDetector_create(threshold=7)
        #fast1 = cv2.FastFeatureDetector_create(threshold=15)
        # find and draw the keypoints
        #cv2.FastFeatureDetector_create()
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
        cv2.rectangle(frame, (0,0), (630,270), (0,0,255), 2)
        cv2.imshow('Computer WebCam',frame)
        #cv2.imshow("External Webcam", frame1)
        #out.write(frame1)
        # Create black (zeroed pixels) image, the same size as the frame
        mask = np.zeros((frame.shape[0],frame.shape[1], 3), np.uint8)
        mask[:] = (0,0,0)

        # Draw the kp's in yellow over the black image
        fmask = cv2.drawKeypoints(mask, kp, None, color=(0, 255, 255), flags=0)

        cv2.imshow('Keypoints only', fmask)
        k = cv2.waitKey(10) & 0xFF
        if k == 27:
            break

except KeyboardInterrupt:
    raise SystemExit