import cv2
import numpy as np
import time
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

class ColourTrack():
    def __init__(self,cam, px_cols, px_rows, redBounds, greenBounds, blueBounds):
        self.r_lowerBound = redBounds[0]
        self.r_upperBound = redBounds[1]
        self.g_lowerBound = greenBounds[0]
        self.g_upperBound = greenBounds[1]
        self.b_lowerBound = blueBounds[0]
        self.b_upperBound = blueBounds[1]
        self.cap = cam
        self.count = 0
        self.found_blue = 0
        self.found_green = 0
        self.found_red = 0
        self.kernelOpen = np.ones((5, 5))
        self.kernelClose = np.ones((20, 20))
        self.b_area_list = []
        self.g_area_list = []
        self.r_area_list = []
        self.font = cv2.FONT_HERSHEY_COMPLEX

        self.ret, self.frame = self.cap.read()
        # Resized to process faster
        self.frame = cv2.resize(self.frame, (720, 540))
        self.r_frame = cv2.resize(self.frame, (px_cols, px_rows))
        # self.r_frame1 = cv2.resize(frame,(340,220))
        self.r_frame = self.denoise(self.r_frame)
        # denoise(self.r_frame1)
        self.frame_HSV = cv2.cvtColor(self.r_frame, cv2.COLOR_BGR2HSV)

    def checkArea(self,area, lower, upper):
        if area > lower and area < upper:
            return 1
        else:
            return 0

    def denoise(self, frame):
        frame = cv2.medianBlur(frame, 5)
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        return frame

    def filter(self):

        # Create filter for red colour
        self.r_mask = cv2.inRange(self.frame_HSV, self.r_lowerBound, self.r_upperBound)
        self.r_maskOpen = cv2.morphologyEx(self.r_mask, cv2.MORPH_OPEN, self.kernelOpen)
        self.r_maskClose = cv2.morphologyEx(self.r_maskOpen, cv2.MORPH_CLOSE, self.kernelClose)
        self.r_maskFinal = self.denoise(self.r_maskClose)

        # Create filter for green colour
        self.g_mask = cv2.inRange(self.frame_HSV, self.g_lowerBound, self.g_upperBound)
        self.g_maskOpen = cv2.morphologyEx(self.g_mask, cv2.MORPH_OPEN, self.kernelOpen)
        self.g_maskClose = cv2.morphologyEx(self.g_maskOpen, cv2.MORPH_CLOSE, self.kernelClose)
        self.g_maskFinal = self.denoise(self.g_maskClose)
        self.g_maskFinal = self.denoise(self.g_maskClose)

        # Create filter for blue colour
        self.b_mask = cv2.inRange(self.frame_HSV, self.b_lowerBound, self.b_upperBound)
        self.b_maskOpen = cv2.morphologyEx(self.b_mask, cv2.MORPH_OPEN, self.kernelOpen)
        self.b_maskClose = cv2.morphologyEx(self.b_maskOpen, cv2.MORPH_CLOSE, self.kernelClose)
        self.b_maskFinal = self.denoise(self.b_maskClose)
        self.b_maskFinal = self.denoise(self.b_maskFinal)

    def makeContours(self):
        # Find contours in the red & yellow masks
        r_im, self.r_contours, r_hier = cv2.findContours(self.r_maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        g_im, self.g_contours, g_hier = cv2.findContours(self.g_maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        b_im, self.b_contours, b_hier = cv2.findContours(self.b_maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        self.contours = [self.b_contours, self.g_contours, self.r_contours]

    def drawFrame(self):
        # Iterate through contours for each colour & draw a box round a sufficient cluster.
        cnt_areas = []

        for i in range(len(self.contours)):
            if i == 0:
                cv2.drawContours(self.r_frame, self.contours[i], -1, (255, 0, 0), 3)
            elif i == 1:
                cv2.drawContours(self.r_frame, self.contours[i], -1, (0, 255, 0), 3)
            else:
                cv2.drawContours(self.r_frame, self.contours[i], -1, (0, 0, 255), 3)
            # cv2.drawContours(self.frame_HSV, contours[i], -1, (0, 255, 255), 3)
            for j in range(len(self.contours[i])):
                x, y, w, h = cv2.boundingRect(self.contours[i][j])
                if i == 0:
                    # print "Blue Height: %s\n Blue Width: %s" % (h,w)
                    # The colour blue
                    colour = (255, 0, 0)
                    cv2.circle(self.r_frame, (x, y), 2, colour, 1)
                    # The area of the blue object contour in rows * cols
                    self.b_area = cv2.contourArea(self.contours[i][j])
                    # Function checks area's within bounds

                    if self.checkArea(self.b_area, 100, 500):
                        # Draws a rectangle around the contour bounds
                        cv2.rectangle(self.r_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                        print "Co-ords: ", (x, y)

                    print "Blue Area: ", self.b_area
                    if self.b_area > 40 and self.count > 3 and len(self.b_area_list) < 3:
                        self.b_area_list.append(self.b_area)
                    elif self.b_area > 40 and len(self.b_area_list) > 2:
                        self.b_area_list.append(self.b_area)
                        b_len = len(self.b_area_list)
                        if (self.b_area_list[b_len - 2] + self.b_area_list[b_len - 1]) / 2 > 40:
                            if self.checkArea(self.b_area, 40, 1000):
                                # print "Blue Object Found"
                                self.found_blue += 1

                elif i == 1:

                    self.g_area = cv2.contourArea(self.contours[i][j])
                    # print "Green Height: %s\n Green Width: %s" % (h, w)
                    colour = (0, 255, 0)
                    cv2.circle(self.r_frame, (x, y), 2, colour, 2)
                    if self.checkArea(self.g_area, 100, 500):
                        cv2.rectangle(self.r_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    print "Green Area: ", self.g_area
                    if self.g_area > 40 and self.count > 3 and len(self.g_area_list) < 3:
                        self.g_area_list.append(self.g_area)
                    elif self.g_area > 40 and len(self.g_area_list) > 2:
                        self.g_area_list.append(self.g_area)
                        g_len = len(self.g_area_list)
                        if (self.g_area_list[g_len - 2] + self.g_area_list[g_len - 1]) / 2 > 40:
                            # print "Green Object Found"
                            self.found_green += 1
                else:
                    cv2.circle(self.r_frame, (x + w, y + h), 2, (0, 0, 255), 4)
                    self.r_area = cv2.contourArea(self.contours[i][j])
                    colour = (0, 0, 255)
                    if self.checkArea(self.r_area, 100, 500):
                        cv2.rectangle(self.r_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    print "Red Area:", self.r_area
                    if self.r_area > 40 and self.count > 3 and len(self.r_area_list) < 3:
                        self.r_area_list.append(self.r_area)

                    elif self.r_area > 40 and len(self.r_area_list) > 2:
                        self.r_area_list.append(self.r_area)
                        r_len = len(self.r_area_list)
                        if (self.r_area_list[r_len - 2] + self.r_area_list[r_len - 1]) / 2 > 40:
                            if self.checkArea(self.r_area, 100, 1000):
                                # print "Red Object Found"
                                self.found_red += 1

                # Write the contour rectangle index in subscript of the rectangle
                cv2.putText(self.r_frame, "%s, %s" % (str(x), str(y)), (x - 20, y + h + 20
                                                                   ), self.font, fontScale=0.5, color=colour, thickness=2)

        # print len(x_list), len(y_list)
        for px in range(px_cols / 40):
            cv2.line(self.r_frame, ((px * 40), 0), ((px * 40), 7), thickness=1, color=(0, 0, 0))
            cv2.putText(self.r_frame, str(px * 40), ((px * 40), 25), color=(0, 0, 0), thickness=1, fontScale=1,
                        fontFace=cv2.FONT_HERSHEY_PLAIN)

            # Show all the windows
        cv2.imshow("Blue Mask", self.b_maskClose)
        cv2.imshow("Red Mask", self.r_maskClose)
        cv2.imshow("Green Mask", self.g_maskClose)
        cv2.imshow("Contoured Frame", self.r_frame)
        if self.count > 20:
            out.write(self.r_frame)
        self.count += 1
        print "\n ----%s----- \n" % str(self.count)


cam = int(args["cam"])
cap = cv2.VideoCapture(cam)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output.avi", fourcc, 10.0, (px_cols,px_rows))


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
