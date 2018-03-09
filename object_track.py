import cv2
import numpy as np
import MyArgs
from ColourTrack import ColourTrack
import argparse

# cd Documents \r cd OpenCV_Scripts \r python object_track.py

px_cols = 1920
px_rows = 1080


args = MyArgs.MyArgs()
arg_lst = args.imcam()
if arg_lst[0] == "im":
    file = arg_lst[1]
    cam = None
elif arg_lst[0] == "cam":
    cam = arg_lst[1]
    file = None
else:
    file = "normal.jpg"
    cam = None


#Upper & lower bounds for general colours
g_list = [np.array([34,100,120]), np.array([100,255,255])]
y_list = [np.array([23,70,210]), np.array([30,255,255])]
r_list = [np.array([0,120,170]),np.array([18, 255,255])]
b_list = [np.array([95,100,100]),np.array([130, 255, 255])]
w_list = [np.array([0,0,200]),np.array([255, 30, 255])]

#HSV Bounds Arrays for LEDs
g_led_list = [np.array([32,46,207]),np.array([59,255,255])]
y_led_list = [np.array([19,0,216]),np.array([28,255,255])]
r_led_list = [np.array([0,0,216]),np.array([5, 255,255])]




# Main loop for the colour track objects

count = 1
while True:
    print "\n ----%s----- \n" % str(count)
    track = ColourTrack(px_cols,px_rows, cam, r_list,g_list,b_list,y_list,w_list,file)
    track.filter()
    track.makeContours()
    track.drawFrame(0.5)
    track.findBridge()
    #print "Objects list: \n", track.objects
    # If the escape key is pressed, close the windows and release the video object
    if count % 50 == 0 :
        track.saveFrame("norm%s.jpg" % str(count/50), "contour%s.jpg"%str(count/50))
    cont_frame = track.r_frame
    count += 1
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break
if cam != None:
    cam.release()
cv2.destroyAllWindows()
