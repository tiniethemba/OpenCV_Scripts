import cv2
import time
cap = cv2.VideoCapture(0)

for i in range(5):
    time.sleep(2)
    r1,f1 = cap.read()
    f1 = cv2.resize(f1, (640,480))
    cv2.imwrite("pic%s.jpg"%str(i), f1)
    time.sleep(1)