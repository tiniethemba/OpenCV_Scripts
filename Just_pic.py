import cv2

cap1 = cv2.VideoCapture(1)
r1,f1 = cap1.read()
f1 = cv2.resize(f1, (640,480))
cv2.imwrite("pic.jpg", f1)
