# TO detect circles in images, the cv2.HoughCircles function is necessary.
# Its signature is: cv2.HoughCircles(image,method,dp,minDist)
# IF image is colored, convert to grayscale first.
# Method - method for circle detection, which currently is cv2.HOUGH_GRADIENT
# dp - Larger dp is, the smaller the accumlator array is.
# minDist - Min dist between centre coordinates of detected circles. If minDist is too small, multiple circles
# in the same area as the real circle might be falsely detected.
# Too small a minDist may not detect larger circles at all.
# import the necessary packages
import numpy as np
import argparse
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())


# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(args["image"])
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect circles in the image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT,1.2,240)

# ensure at least some circles were found
if circles is not None:
    #convert the (x,y) co-ords & cricle radii to integers
    circles = np.round(circles[0,:]).astype("int")

    # loop over the (x,y) coordinates and circle radii
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 0, 255), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        # show the output image
    cv2.imshow("output", np.hstack([image, output]))
    cv2.imshow("OP_alone", output)
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        raise SystemExit
else:
    print "Couldn't find any circles!"
    raise SystemExit