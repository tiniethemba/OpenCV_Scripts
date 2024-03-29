import cv2
import numpy as np
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--cam")
ap.add_argument("-i", "--im")
args = vars(ap.parse_args())

# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100


def nothing(x):
    pass
def denoise(x):
    x = cv2.medianBlur(x, 5)
    x = cv2.GaussianBlur(x,(5,5), 0)
    return x
# Creating track bar
cv2.createTrackbar('h', 'result', 0, 179, nothing)
cv2.createTrackbar('s', 'result', 0, 255, nothing)
cv2.createTrackbar('v', 'result', 0, 255, nothing)
print args
print args.get("im", 0)

if args.get("im",0):
    my_image = args["im"]
else:
    cam_index = int(args["cam"])
    cap = cv2.VideoCapture(cam_index)


# Creating track bar
cv2.createTrackbar('h', 'result',0,179,nothing)
cv2.createTrackbar('s', 'result',0,255,nothing)
cv2.createTrackbar('v', 'result',0,255,nothing)
while(1):
    if args.get("im", 0):
        frame = cv2.imread(my_image)

    else:
        _, frame = cap.read()
    frame = cv2.resize(frame, (480, 360))
    frame = denoise(frame)
    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h','result')
    s = cv2.getTrackbarPos('s','result')
    v = cv2.getTrackbarPos('v','result')

    # Normal masking algorithm
    lower_blue = np.array([h,s,v])
    upper_blue = np.array([255,100,180])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)

    result = cv2.bitwise_and(frame,frame,mask = mask)
    cv2.imshow('result', result)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

if args.get("cam", 0):
    cap.release()

cv2.destroyAllWindows()