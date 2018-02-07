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

def do_image(image1):
    while (1):
        image = cv2.imread(image1)
        image = cv2.resize(image, (1200, 960))
        image = denoise(image)
        # converting to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # get info from track bar and appy to result
        h = cv2.getTrackbarPos('h', 'result')
        s = cv2.getTrackbarPos('s', 'result')
        v = cv2.getTrackbarPos('v', 'result')

        # Normal masking algorithm
        lower_blue = np.array([h, s, v])
        upper_blue = np.array([35, 255, 255])
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
        result = cv2.bitwise_and(image, image, mask=mask)
        cv2.imshow('result', result)
        #cv2.imshow("mask", mask)
        cv2.imshow('image', image)

        key = cv2.waitKey(10) & 0xff
        if key == 27:
            break
    cv2.destroyAllWindows()
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
    upper_blue = np.array([80,255,255])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)

    result = cv2.bitwise_and(frame,frame,mask = mask)
    cv2.imshow('result', result)
    cv2.imshow("mask", mask)
    cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break


cap.release()

cv2.destroyAllWindows()