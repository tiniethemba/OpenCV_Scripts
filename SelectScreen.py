import ColourTrack
import cv2
import GetHSV
import MyArgs
import numpy as np
import pytesseract as tess
from PIL import Image

px_cols = 640
px_rows = 480

b_list = [np.array([80,50,140]),np.array([110, 185, 255])]

class SelectScreen():
    def __init__(self, px_cols, px_rows, blueBounds, filename):
        self.ct = ColourTrack.ColourTrack(px_cols, px_rows, 0, blueBounds=blueBounds, filename=filename)
        self.ct.filter()
        self.ct.makeContours()
        self.ct.drawFrame()
        self.min_area = px_cols * px_rows / 100  # 1 percent of frame area
        self.max_area = self.min_area * 4  # 4 percent of frame area
        # For each contoured frame find it's area value

    def crop(self):

        for c in self.ct.co_ord_list:
            if self.ct.checkArea(self.ct.objects[str(c)]['area'], self.min_area, self.max_area):
                # If the area is big enough, save its box_co-ordinates
                crop_coords = self.ct.objects[str(c)]['co-ords']
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
                cropped = self.ct.frame[first2:second2,first1:second1]
                #cropped = ct.frame
                # Show the cropped image of the screen
                #cv2.imshow("cropped", cropped)
                self.cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

    def get_letters(self):
        cv2.imshow("1st cropped", self.cropped)
        get_letters = self.ct.auto_canny(self.cropped)
        cv2.imshow("cropped", get_letters)
        self.letters = tess.image_to_string(Image.fromarray(get_letters)).encode("utf-8")
        self.letters_list = list(self.letters)
        self.desired_str = "EQUALequal"
        self.continue_str = "0.0B"
        self.des_count = 0
        self.cont_count = 0
        for des in self.desired_str:
            if des in self.letters:
                self.des_count+=1
        if self.des_count > 3:
            print "STOP TURNING!!!!!"


        for cont in self.continue_str:
            if cont in self.letters:
                self.cont_count+=1
        if self.cont_count > 2:
            print "KEEP TURNING!!!!!"
        print self.letters
        print self.cont_count

args = MyArgs.MyArgs()
arg_lst = args.imcam()
if arg_lst[0] == "im":
    file = arg_lst[1]
elif arg_lst[0] == "cam":
    cam = int(arg_lst[1])
    cam = cv2.VideoCapture(cam)
else: file = "LCD.png"
ss = SelectScreen(px_cols,px_rows,b_list, file)
ss.crop()
ss.get_letters()



#for k, v in ct.objects.items():
    #print "Key:", k
    #print "Value", v


while(1):
    key = cv2.waitKey(10) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()