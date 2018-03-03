import ColourTrack
import cv2
import GetHSV
import numpy as np
import pytesseract as tess
from PIL import Image

px_cols = 640
px_rows = 480



b_list = [np.array([80,50,140]),np.array([110, 185, 255])]

ct = ColourTrack.ColourTrack(px_cols, px_rows,0, blueBounds = b_list, filename = "pic15.jpg")
ct.filter()
ct.makeContours()
ct.drawFrame()
min_area = px_cols * px_rows / 100 # 1 percent of frame area
max_area = min_area * 4 # 4 percent of frame area
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
        pixel1 = [a1,b1,c1,d1]
        pixel2 = [a2, b2, c2, d2]
        count1 = 0
        count2 = 0

        for p1 in pixel1:
            cur_value = pixel1[count1]
            if pixel1.count(cur_value) > 1:
                pixel1.pop(count1)
            count1+=1
        first1, second1 = pixel1

        for p2 in pixel2:
            cur_value = pixel2[count2]
            pixel2.count(cur_value)
            if pixel2.count(cur_value) > 1:
                pixel2.pop(count2)
            count2 += 1
        first2, second2 = pixel2

        # Crop the original frame
        cropped = ct.frame[  first2:second2,first1:second1]
        #cropped = ct.frame
        # Show the cropped image of the screen
        #cv2.imshow("cropped", cropped)
        cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        cv2.imshow("1st cropped", cropped)
        get_letters = ct.auto_canny(cropped)
        cv2.imshow("cropped", get_letters)
        print tess.image_to_string(Image.fromarray(get_letters)).encode("utf-8")


#for k, v in ct.objects.items():
    #print "Key:", k
    #print "Value", v


while(1):
    key = cv2.waitKey(10) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()