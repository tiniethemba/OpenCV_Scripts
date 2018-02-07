import numpy as np
import argparse
import cv2

# construct the argument pasrse and parse the arguments

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

# load the image
if __name__ == "__main__":
    image = cv2.imread(args["image"])
    image1 = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

height, width = image1.shape[:2]
image = cv2.resize(image,(width/3,height/2), interpolation= cv2.INTER_AREA)
image1 = cv2.resize(image1,(width/3,height/2), interpolation= cv2.INTER_AREA)

#define the list of boundaries
# Descending: (Red), (Blue), (Yellow), (Green)
boundaries = [([0,50,50],[10,255,255]),
              ([110,100,100],[130,255,235]),
              ([20,100,100],[40,255,255]),
              ([50,100,100],[70,255,200])
              ]
hsv_red_low = np.uint8([[[0,50,50]]])
hsv_red_high = np.uint8([[[10,255,255]]])
bgr_red_low = cv2.cvtColor(hsv_red_low,cv2.COLOR_HSV2BGR)
bgr_red_high = cv2.cvtColor(hsv_red_high,cv2.COLOR_HSV2BGR)
my_red = np.uint8([[[0,0,255]]])
my_green = np.uint8([[[0,255,50]]])
bgr_yellow = np.uint8([[[0,255,255]]])
my_bgr_blue = np.uint8([[[255,0,0]]])
hsv_red = cv2.cvtColor(my_red, cv2.COLOR_BGR2HSV)
hsv_yellow = cv2.cvtColor(bgr_yellow, cv2.COLOR_BGR2HSV)
hsv_blue = cv2.cvtColor(my_bgr_blue, cv2.COLOR_BGR2HSV)
hsv_green = cv2.cvtColor(my_green, cv2.COLOR_BGR2HSV)
print hsv_red, "\n"
print hsv_blue, "\n"
print hsv_green, "\n"
print hsv_yellow, "\n"
print "HSV RED LOW", bgr_red_low
print "HSV RED HIGH", bgr_red_high
print "HSV YELLOW HIGH ", hsv_yellow
# loop over the boundaries
for (lower, upper) in boundaries:
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(image1, lower, upper)
    output = cv2.bitwise_and(image1, image1, mask=mask)
    output = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)
    # show the images
    cv2.imshow("Images",np.hstack([image, output]))
    cv2.waitKey(0)