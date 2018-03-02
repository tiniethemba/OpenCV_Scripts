import ColourTrack
import cv2
import GetHSV
import numpy as np

px_cols = 640
px_rows = 480



b_list = [np.array([80,40,140]),np.array([110, 255, 255])]
cap = cv2.VideoCapture(0)
ct = ColourTrack.ColourTrack(cap, px_cols, px_rows, blueBounds = b_list, video_mode = 0,filename = "LCD.png")
ct.filter()
ct.makeContours()
ct.drawFrame()
min_area = px_cols * px_rows / 100
max_area = min_area * 4
# For each contoured frame find it's area value


for c in ct.co_ord_list:
    if ct.checkArea(ct.objects[str(c)]['area'], min_area, max_area):
        # If the area is big enough, save its box_co-ordinates
        crop_coords = ct.objects[str(c)]['co-ords']
        # Unpack to get individual pixels for cropping
        a, b, c, d = crop_coords
        a1, a2 = a
        b1, b2 = b
        c1, c2 = c
        d1, d2 = d
        # Crop the original frame
        cropped = ct.frame[d2:b2, b1:a1]
        # Show the cropped image of the screen
        cv2.imshow("cropped", cropped)


for k, v in ct.objects.items():
    print "Key:", k
    print "Value", v


while(1):
    key = cv2.waitKey(10) & 0xFF
    if key == 27:
        break