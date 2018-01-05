import cv2

cap1 = cv2.VideoCapture(1)
r1,f1 = cap1.read()
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("test.avi", fourcc, 10.0, (640,480))
while (True):
    r,frame = cap1.read()
    out.write(frame)
    cv2.imshow("frame", frame)
    esc = cv2.waitKey(100) & 0xFF
    if esc == 27:
        break
cap1.release()
cv2.destroyAllWindows()