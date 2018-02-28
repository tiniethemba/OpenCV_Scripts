import MyArgs
import ColourFilter as cl
import GetHSV
from PIL import Image
import pytesseract as tess
import cv2
import numpy as np

hsv_range = [np.array([0, 0, 0]), np.array([110, 255, 255])]
args = MyArgs.MyArgs()

BINARY_THREHOLD = 180

# Get frame(s) depending on whether image or video
cam_type = args.imcam()
if "im" in cam_type:
    frame = cv2.imread(cam_type[1])
elif "cam" in cam_type:
    _, frame = cam_type[1].read()
else:
    print "Something's gone wrong here."


def auto_canny(image, lower = 120, upper = 180):
    filtered = cv2.adaptiveThreshold(image.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15,3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    or_image = cv2.bitwise_or(image, closing)
    edged = cv2.Canny(or_image, lower, upper)
    # return the edged image
    return edged

## FInd the desired HSV values
get_values = GetHSV.getHSV(640,480)
lower = get_values.getHSV()
lower = np.array([lower[0], lower[1], lower[2]])
#print "HSV lower", lower
#lower = np.array([84,50,240])
## Filter out all the features in the frame that aren't the frame
filt = cl.ColourFilter(frame, lower, hsv_range[1])
mask = filt.filt()

## Convert that frame from HSV to grayscale
grey = cv2.bitwise_or(frame,frame,mask = mask)
while(1):
    cv2.imshow("grey", grey)
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break
#grey = cv2.resize(grey,dsize = (0,0),fx = ,fy = 1.2)
bgr = cv2.cvtColor(grey, cv2.COLOR_HSV2BGR)
grey = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(grey,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)

cv2.imshow("g",thresh)
k = cv2.waitKey(5) & 0xFF
thresh = auto_canny(grey)
sh = thresh.shape
thresh = thresh[sh[0]/2:sh[0],0:sh[1]]
print tess.image_to_string(Image.fromarray(thresh)).encode("utf-8")
while(1):
    cv2.imshow("t", thresh)
    k = cv2.waitKey(10) & 0xff
    if k == 27:
        break
#if k == 27:
#     break
## Perform Tesseract on that



