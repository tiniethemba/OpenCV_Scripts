import cv2
import time
cap1 = cv2.VideoCapture(1)
for i in range(20):
    r1,f1 = cap1.read()
    f1 = cv2.resize(f1, (640,480))
    cv2.imwrite("pic%s.jpg"%str(i), f1)
    time.sleep(1)