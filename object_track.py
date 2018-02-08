import cv2
import numpy as np
from ColourTrack import ColourTrack
import argparse

# cd Documents \r cd OpenCV_Scripts \r python object_track.py

px_cols = 1280
px_rows = 960


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--cam", required=True,
	help="Camera Index (from 0 to number of connected webcams)")
args = vars(ap.parse_args())

#Upper & lower bounds for general colours
g_list = [np.array([34,100,40]), np.array([100,255,255])]
y_list = [np.array([13,20,60]), np.array([20,255,255])]
r_list = [np.array([0,140,200]),np.array([17, 255,255])]
b_list = [np.array([95,60,80]),np.array([130, 255, 255])]

#HSV Bounds Arrays for LEDs
g_led_list = [np.array([32,46,207]),np.array([59,255,255])]
y_led_list = [np.array([19,0,216]),np.array([28,255,255])]
r_led_list = [np.array([0,0,216]),np.array([5, 255,255])]


cam = int(args["cam"])
cap = cv2.VideoCapture(cam)


# Main loop for the colour track objects
r,f = cap.read()
while True:
    track = ColourTrack(cap,px_cols,px_rows,r_list,g_list,b_list)
    track.filter()
    track.makeContours()
    track.drawFrame()

    # If the escape key is pressed, close the windows and release the video object
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
