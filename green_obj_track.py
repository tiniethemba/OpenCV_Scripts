import cv2
import numpy as np

#Upper & lower bounds for colour green
lowerBound = np.array([31,80,40])
upperBound = np.array([50,255,255])#

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
cap = cv2.VideoCapture(1)

#ont =cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX,2,0.5,0,3,1)
font = cv2.FONT_HERSHEY_COMPLEX
r,f = cap.read()
while True:
    ret, frame = cap.read()
    #Resized to process faster
    frame = cv2.resize(frame,(340,220))
    frame_HSV = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # Create filter for green colour
    g_mask = cv2.inRange(frame_HSV, lowerBound, upperBound)


    g_maskOpen=cv2.morphologyEx(g_mask,cv2.MORPH_OPEN,kernelOpen)
    g_maskClose=cv2.morphologyEx(g_maskOpen,cv2.MORPH_CLOSE,kernelClose)
    g_maskFinal = g_maskClose
    im,contours,hier = cv2.findContours(g_maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(frame,contours,-1,(0,255,255),3)
    for i in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[i])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, str(i + 1), (x-10, y+h+10), font, fontScale = 0.75, color =  (25, 0, 0), thickness = 2)
        #cv2.putText()
    cv2.imshow("g_maskClose", g_maskClose)
    cv2.imshow("g_maskOpen", g_maskOpen)
    cv2.imshow("cam", frame)
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break