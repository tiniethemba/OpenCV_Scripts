from ColourTrack import ColourTrack
import cv2
import MyArgs
import numpy as np
import pytesseract as tess
import talker
import time
from PIL import Image

px_cols = 640
px_rows = 480

mbed_lcd = [np.array([80,30,140]),np.array([110, 100, 255])]
testing = [np.array([80,50,100]),np.array([110, 255, 255])]

class SelectScreen():
    def __init__(self, px_cols, px_rows, blueBounds, filename = None, cam = None):
        self.ct = ColourTrack(px_cols, px_rows, cam = cam, blueBounds=blueBounds, screen = 1)
        self.min_area = px_cols * px_rows / 100# 4 percent of frame area
        self.max_area = self.min_area * 50  # 50 percent of frame area
        self.large_con = 0
        self.ct.filter()
        self.ct.makeContours()
        self.ct.drawFrame()

    # For each contoured frame find it's area value
    def crop(self, c):
        self.large_con +=1
        # If the area is big enough, save its box_co-ordinates
        crop_coords = self.ct.objects[str(c)]['co-ords']
        # Unpack to get individual pixels for cropping
        a, b, c, d = crop_coords
        ax, ay = a
        bx, by = b
        cx, cy = c
        dx, dy = d
        ##### Need x & y from A, x from B, and y from C
        ###### Cropping Format is img[y1:y2,x1:x2]

        y = [dy,by]
        x = [bx,dx]

        #cv2.imshow("cropped", cropped)
        #self.crop = cropped


        if self.large_con:
            return [y,x]
        else:
            return [(220,310), (240,330)]

    def get_letters(self, im = None):
        # Perform pre-processing on the cropped image
        if im is not None:
            self.get_letters = self.ct.auto_canny(im)

            cv2.imshow("after_canny.jpg", self.get_letters)
            # Run the Tesseract engine to get string
            self.letters = tess.image_to_string(Image.fromarray(self.get_letters)).encode("utf-8")

            # Separate string into characters
            self.letters_list = list(self.letters)

            #Initalisations for the next step's process
            self.desired_str = "EQUALequal"
            self.continue_str = "42.8B"
            self.des_count = 0
            self.cont_count = 0

            # Print for Debug
            print self.letters

            # Check if screen string matches desired.
            for des in self.desired_str:
                if des in self.letters:
                    self.des_count+=1
            if self.des_count > 3:
                print "STOP TURNING!!!!!"

            # Check if screen string matches the string for continuing
            for cont in self.continue_str:
                if cont in self.letters:
                    self.cont_count+=1
            if self.cont_count > 2:
                print "PLEASE TURN RIGHT!!"

    def ROS_pub(self, message = None, image = None, topic = None, rate = None):
        talk = talker.Talker(message,topic,rate)
        if message !=  None:
            talk.talker()

args = MyArgs.MyArgs()
arg_lst = args.imcam()
if arg_lst[0] == "im":
    file = arg_lst[1]
elif arg_lst[0] == "cam":
    cam = cv2.VideoCapture(arg_lst[1])
    file = None
elif arg_lst[0] == "vid":
    vid = arg_lst[1]
    cam = cv2.VideoCapture(str(vid))
    file = None
else:
    file = "LCD.png"
    cam = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("FinalResult.avi", fourcc, 20.0)


loop_count = 0
while True:

    ss = SelectScreen(px_cols, px_rows, mbed_lcd, cam=cam)
    if not ss.ct.ret:
        break

    if loop_count > 40:
        # Find blue rectangle and crop the frame to its co-ords
        for c in ss.ct.co_ord_list:
            if ss.ct.checkArea(ss.ct.objects[str(c)]['area'], ss.min_area, ss.max_area) and ss.ct.objects[str(c)]['type'] == "Screen":
                y,x = ss.crop(c)
                #print y,x
                ###### Cropping Format is img[y1:y2,x1:x2]

                #print "Pixels", p1a,p1b,p2a,p2b
                crop = ss.ct.r_frame[min(y):max(y),min(x):max(x)]
                try:
                    cv2.imshow("C",crop)
                except cv2.error:
                    cv2.imwrite("LastFrame.jpg",ss.ct.r_frame)
                # Convert frame into greyscale

                crop_grey = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

                # Preprocess image & run the Tesseract engine to get the on-screen letters.
                ss.get_letters(crop_grey)
                out.write(ss.get_letters)


    key = cv2.waitKey(10) & 0xFF

    # Exit if ESC key pressed
    if key == 27:
        break

    loop_count += 1
if cam != None:
    cam.release()

cv2.destroyAllWindows()