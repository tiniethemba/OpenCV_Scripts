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

mbed_lcd = [np.array([80,50,140]),np.array([110, 185, 255])]
testing = [np.array([80,50,100]),np.array([110, 255, 255])]

class SelectScreen():
    def __init__(self, px_cols, px_rows, blueBounds, filename = None, cam = None):
        self.ct = ColourTrack(px_cols, px_rows, cam = cam, blueBounds=blueBounds, screen = 1)
        self.min_area = px_cols * px_rows / 10  # 10 percent of frame area
        self.max_area = self.min_area * 5  # 50 percent of frame area
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
        #pixel1 = [a1,c1]
        #pixel2 = [a2,b2]
        ##### Need x & y from A, x from B, and y from C

        print "B equals", b

        print "D equals",d
        count1 = 0
        count2 = 0


        ###### Cropping Format is img[y1:y2,x1:x2]

        y = [dy,by]
        x = [bx,dx]

        #cv2.imshow("cropped", cropped)
        #self.crop = cropped
        #self.crop_grey = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)

        if self.large_con:
            return [y,x]
        else:
            return [(220,310), (240,330)]




    def get_letters(self, im = None):
        # Perform pre-processing on the cropped image
        get_letters = self.ct.auto_canny(im)

        cv2.imshow("after_canny.jpg", get_letters)
        # Run the Tesseract engine to get string
        self.letters = tess.image_to_string(Image.fromarray(get_letters)).encode("utf-8")

        # Separate string into characters
        self.letters_list = list(self.letters)

        #Initalisations for the next step's process
        self.desired_str = "EQUALequal"
        self.continue_str = "0.0B"
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
            print "KEEP TURNING!!!!!"


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
#elif arg_lst[0] == "vid":
#    vid = arg_lst[1]
#    cam = cv2.VideoCapture(str(vid))
#    file = None
else:
    file = "LCD.png"
    cam = cv2.VideoCapture(0)





loop_count = 0
while True:

    ss = SelectScreen(px_cols, px_rows, testing, cam=cam)
    if not ss.ct.ret:
        break

    if loop_count > 40:
        # Find blue rectangle and crop the frame to its co-ords
        for c in ss.ct.co_ord_list:
            if ss.ct.checkArea(ss.ct.objects[str(c)]['area'], ss.min_area, ss.max_area) and ss.ct.objects[str(c)]['type'] == "Screen":
                y,x = ss.crop(c)
                print y,x
                ###### Cropping Format is img[y1:y2,x1:x2]

                #print "Pixels", p1a,p1b,p2a,p2b
                crop = ss.ct.r_frame[min(y):max(y),min(x):max(x)]
                try:
                    cv2.imshow("C",crop)
                except cv2.error:
                    cv2.imwrite("LastFrame.jpg",ss.ct.r_frame)

    # Run the Tesseract engine to get the on-screen letters.
    #if im != 0 :
    #     #print "Out of class", type(ss.crop)
    #     if 'None' not in str(type(im)):
    #         print type(im)
    #     cv2.imshow("crop", im)
    #Send the resulting frame to ROS

    #for k, v in ss.ct.objects.items():
    #    print "Key:", k
    #    print "Value", v

    ## ss.ROS_pub()
    #cv2.imwrite("My_frame.jpg", ss.ct.frame)
    #cv2.imwrite("R_frame.jpg", ss.ct.r_frame)
    key = cv2.waitKey(10) & 0xFF

    # Exit if ESC key pressed
    if key == 27:
        break

    loop_count += 1
    #time.sleep(0.01)
if cam != None:
    cam.release()

cv2.destroyAllWindows()