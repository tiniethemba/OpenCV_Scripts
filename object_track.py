import cv2
import numpy as np
from ColourTrack import ColourTrack
import argparse

# cd Documents \r cd OpenCV_Scripts \r python object_track.py

px_cols = 1920
px_rows = 1080
filename = "normal.jpg"


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--cam", required=True,
	help="Camera Index (from 0 to number of connected webcams)")
args = vars(ap.parse_args())

#Upper & lower bounds for general colours
g_list = [np.array([34,100,120]), np.array([100,255,255])]
y_list = [np.array([23,40,210]), np.array([30,255,255])]
r_list = [np.array([0,120,170]),np.array([18, 255,255])]
b_list = [np.array([95,100,100]),np.array([130, 255, 255])]
w_list = [np.array([0,0,180]),np.array([255, 30, 255])]

#HSV Bounds Arrays for LEDs
g_led_list = [np.array([32,46,207]),np.array([59,255,255])]
y_led_list = [np.array([19,0,216]),np.array([28,255,255])]
r_led_list = [np.array([0,0,216]),np.array([5, 255,255])]


cam = int(args["cam"])
cap = cv2.VideoCapture(cam)


# Main loop for the colour track objects
r,f = cap.read()
count = 1
while True:
    print "\n ----%s----- \n" % str(count)
    track = ColourTrack(px_cols,px_rows, cap, r_list,g_list,b_list,y_list,w_list,filename)
    track.filter()
    track.makeContours()
    track.drawFrame(0.5)
    print "Objects list: \n", track.objects
    # If the escape key is pressed, close the windows and release the video object
    if count % 50 == 0 :
        track.saveFrame("norm%s.jpg" % str(count/50), "contour%s.jpg"%str(count/50))
    cont_frame = track.r_frame
    count += 1
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
