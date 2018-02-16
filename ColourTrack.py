import cv2
import numpy as np

class ColourTrack():
    def __init__(self,cam, px_cols, px_rows, redBounds, greenBounds, blueBounds, yellowBounds = None, whiteBounds = None):
        self.r_lowerBound = redBounds[0]
        self.r_upperBound = redBounds[1]
        self.g_lowerBound = greenBounds[0]
        self.g_upperBound = greenBounds[1]
        self.b_lowerBound = blueBounds[0]
        self.b_upperBound = blueBounds[1]
        self.y_lowerBound = yellowBounds[0]
        self.y_upperBound = yellowBounds[1]
        self.w_lowerBound = whiteBounds[0]
        self.w_upperBound = whiteBounds[1]
        self.blue = (255,0,0)
        self.green = (0,255,0)
        self.red = (0,0,255)
        self.yellow = (0,255,255)
        self.white = (0,0,0)
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
        self.y_area_list = []
        self.w_area_list = []
        self.font = cv2.FONT_HERSHEY_COMPLEX
        self.px_cols = px_cols
        self.px_rows = px_rows
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.out = cv2.VideoWriter("output.avi", self.fourcc, 10.0, (self.px_cols, self.px_rows))
        if redBounds == None:
            self.red = 0
        else: self.red = 1
        if greenBounds == None:
            self.green = 0
        else: self.green = 1
        if blueBounds == None:
            self.blue = 0
        else: self.blue = 1
        if yellowBounds == None:
            self.yellow = 0
        else: self.yellow = 1
        if whiteBounds == None:
            self.white = 0
        else: self.white = 1

        self.ret, self.frame = self.cap.read()

        # Resized to process faster
        self.frame = cv2.resize(self.frame, (720, 540))
        self.r_frame = cv2.resize(self.frame, (self.px_cols, self.px_rows))
        self.grey = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        # self.r_frame1 = cv2.resize(frame,(340,220))
        self.r_frame = self.denoise(self.r_frame)
        # denoise(self.r_frame1)
        self.frame_HSV = cv2.cvtColor(self.r_frame, cv2.COLOR_BGR2HSV)

    def checkArea(self, area, lower, upper):
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
        if self.red:
            self.r_mask = cv2.inRange(self.frame_HSV, self.r_lowerBound, self.r_upperBound)
            self.r_maskOpen = cv2.morphologyEx(self.r_mask, cv2.MORPH_OPEN, self.kernelOpen)
            self.r_maskClose = cv2.morphologyEx(self.r_maskOpen, cv2.MORPH_CLOSE, self.kernelClose)
            self.r_maskFinal = self.denoise(self.r_maskClose)

        if self.green:
        # Create filter for green colour
            self.g_mask = cv2.inRange(self.frame_HSV, self.g_lowerBound, self.g_upperBound)
            self.g_maskOpen = cv2.morphologyEx(self.g_mask, cv2.MORPH_OPEN, self.kernelOpen)
            self.g_maskClose = cv2.morphologyEx(self.g_maskOpen, cv2.MORPH_CLOSE, self.kernelClose)
            self.g_maskFinal = self.denoise(self.g_maskClose)
            self.g_maskFinal = self.denoise(self.g_maskClose)

        if self.blue:
            # Create filter for blue colour
            self.b_mask = cv2.inRange(self.frame_HSV, self.b_lowerBound, self.b_upperBound)
            self.b_maskOpen = cv2.morphologyEx(self.b_mask, cv2.MORPH_OPEN, self.kernelOpen)
            self.b_maskClose = cv2.morphologyEx(self.b_maskOpen, cv2.MORPH_CLOSE, self.kernelClose)
            self.b_maskFinal = self.denoise(self.b_maskClose)
            self.b_maskFinal = self.denoise(self.b_maskFinal)

        if self.yellow:
        # Create filter for yellow colour
            self.y_mask = cv2.inRange(self.frame_HSV, self.y_lowerBound, self.y_upperBound)
            self.y_maskOpen = cv2.morphologyEx(self.y_mask, cv2.MORPH_OPEN, self.kernelOpen)
            self.y_maskClose = cv2.morphologyEx(self.y_maskOpen, cv2.MORPH_CLOSE, self.kernelClose)
            self.y_maskFinal = self.denoise(self.y_maskClose)
            self.y_maskFinal = self.denoise(self.y_maskFinal)

        if self.white:
            # Create filter for yellow colour
            self.w_mask = cv2.inRange(self.frame_HSV, self.w_lowerBound, self.w_upperBound)
            self.w_maskOpen = cv2.morphologyEx(self.w_mask, cv2.MORPH_OPEN, self.kernelOpen)
            self.w_maskClose = cv2.morphologyEx(self.w_maskOpen, cv2.MORPH_CLOSE, self.kernelClose)
            self.w_maskFinal = self.denoise(self.w_maskClose)
            self.w_maskFinal = self.denoise(self.w_maskFinal)

    def adaptive(self):
        pass

    def makeContours(self):

        # Find contours in the red & yellow masks
        r_im, self.r_contours, r_hier = cv2.findContours(self.r_maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        g_im, self.g_contours, g_hier = cv2.findContours(self.g_maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        b_im, self.b_contours, b_hier = cv2.findContours(self.b_maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        y_im, self.y_contours, y_hier = cv2.findContours(self.y_maskFinal.copy(), cv2.RETR_EXTERNAL,
                                                         cv2.CHAIN_APPROX_NONE)
        w_im, self.w_contours, w_hier = cv2.findContours(self.w_maskFinal.copy(), cv2.RETR_EXTERNAL,
                                                         cv2.CHAIN_APPROX_NONE)
        self.contours = [self.b_contours, self.g_contours, self.r_contours, self.y_contours, self.w_contours]

    def drawFrame(self):

        # Iterate through contours for each colour & draw a box round a sufficient cluster.

        for i in range(len(self.contours)):
            #if self.contours[i] == None:
                #self.contours.pop(i)
            if i == 0:
                colors = (255,0,0)
                cv2.drawContours(self.r_frame, self.contours[i], -1, colors, 3)
            elif i == 1:
                colors = (0,255,0)
                cv2.drawContours(self.r_frame, self.contours[i], -1, colors, 3)
            elif i == 2:
                colors = (0,0,255)
                cv2.drawContours(self.r_frame, self.contours[i], -1, colors, 3)
            elif i == 3:
                colors = (0,255,255)
                cv2.drawContours(self.r_frame, self.contours[i], -1, colors, 3)
            elif i == 4:
                colors = (255,255,255)
                cv2.drawContours(self.r_frame, self.contours[i], -1, colors, 3)

            # cv2.drawContours(self.frame_HSV, contours[i], -1, (0, 255, 255), 3)
            the_area = 0
            for j in range(len(self.contours[i])):
                x, y, w, h = cv2.boundingRect(self.contours[i][j])
                if i == 0:
                    # print "Blue Height: %s\n Blue Width: %s" % (h,w)
                    # The colour blue
                    colour = (255,0,0)
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
                    the_area = self.b_area

                elif i == 1:

                    self.g_area = cv2.contourArea(self.contours[i][j])
                    # print "Green Height: %s\n Green Width: %s" % (h, w)
                    colour = (0,255,0)
                    cv2.circle(self.r_frame, (x, y), 2, colour, 2)
                    if self.checkArea(self.g_area, 100, 500):
                        cv2.rectangle(self.r_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    print "Green Area: ", self.g_area
                    print "Co-ords: ", (x, y)
                    if self.g_area > 40 and self.count > 3 and len(self.g_area_list) < 3:
                        self.g_area_list.append(self.g_area)
                    elif self.g_area > 40 and len(self.g_area_list) > 2:
                        self.g_area_list.append(self.g_area)
                        g_len = len(self.g_area_list)
                        if (self.g_area_list[g_len - 2] + self.g_area_list[g_len - 1]) / 2 > 40:
                            # print "Green Object Found"
                            self.found_green += 1
                    the_area = self.g_area
                elif i==2:
                    colour = (0,0,255)
                    cv2.circle(self.r_frame, (x + w, y + h), 2, colour, 4)
                    self.r_area = cv2.contourArea(self.contours[i][j])
                    if self.checkArea(self.r_area, 100, 500):
                        cv2.rectangle(self.r_frame, (x, y), (x + w, y + h), colour, 2)
                    print "Red Area:", self.r_area
                    print "Co-ords: ", (x, y)
                    if self.r_area > 40 and self.count > 3 and len(self.r_area_list) < 3:
                        self.r_area_list.append(self.r_area)

                    elif self.r_area > 40 and len(self.r_area_list) > 2:
                        self.r_area_list.append(self.r_area)
                        r_len = len(self.r_area_list)
                        if (self.r_area_list[r_len - 2] + self.r_area_list[r_len - 1]) / 2 > 40:
                            if self.checkArea(self.r_area, 100, 1000):
                                # print "Red Object Found"
                                self.found_red += 1
                    the_area = self.r_area

                elif i == 3:
                    colour = (0,255,255)
                    self.y_area = cv2.contourArea(self.contours[i][j])
                    # print "Green Height: %s\n Green Width: %s" % (h, w)
                    cv2.circle(self.r_frame, (x, y), 2, colour, 2)
                    if self.checkArea(self.y_area, 100, 500):
                        cv2.rectangle(self.r_frame, (x, y), (x + w, y + h), colour, 2)
                    print "Yellow Area: ", self.y_area
                    print "Co-ords: ", (x, y)
                    if self.y_area > 40 and self.count > 3 and len(self.y_area_list) < 3:
                        self.y_area_list.append(self.y_area)
                    elif self.y_area > 40 and len(self.y_area_list) > 2:
                        self.y_area_list.append(self.y_area)
                        y_len = len(self.y_area_list)
                        if (self.y_area_list[y_len - 2] + self.y_area_list[y_len - 1]) / 2 > 40:
                            # print "Green Object Found"
                            self.found_green += 1
                    the_area = self.y_area
                elif i == 4:
                    colour = (0,0,0)
                    self.w_area = cv2.contourArea(self.contours[i][j])
                    # print "Green Height: %s\n Green Width: %s" % (h, w)
                    cv2.circle(self.r_frame, (x, y), 2, colour, 2)
                    if self.checkArea(self.w_area, 1000, 10000):
                        cv2.rectangle(self.r_frame, (x, y), (x + w, y + h), colour, 2)
                    print "White Area: ", self.w_area
                    if self.w_area > 40 and self.count > 3 and len(self.w_area_list) < 3:
                        self.w_area_list.append(self.w_area)
                    elif self.w_area > 40 and len(self.w_area_list) > 2:
                        self.w_area_list.append(self.w_area)
                        w_len = len(self.w_area_list)
                        if (self.w_area_list[w_len - 2] + self.w_area_list[w_len - 1]) / 2 > 40:
                            # print "Green Object Found"
                            self.found_green += 1
                    the_area = self.w_area
                else:
                    print "Oh Oh, spaghetti-o's!!"
                # Write the contour rectangle index in subscript of the rectangle
                if self.checkArea(the_area, 500, 1000000):
                    cv2.putText(self.r_frame, "%s, %s" % (str(x), str(y)), (x - 40, y + 45
                                                                   ), self.font, fontScale=0.5, color=colour, thickness=2)

        # print len(x_list), len(y_list)
        for px in range(self.px_cols / 40):
            cv2.line(self.r_frame, ((px * 40), 0), ((px * 40), 7), thickness=1, color=(0, 0, 0))
            cv2.putText(self.r_frame, str(px * 40), ((px * 40), 25), color=(0, 0, 0), thickness=1, fontScale=1,
                        fontFace=cv2.FONT_HERSHEY_PLAIN)

            # Show all the windows
        cv2.imshow("White Mask", self.r_maskClose)
        cv2.imshow("Contoured Frame", self.r_frame)
        self.grey = cv2.adaptiveThreshold(self.grey, 155, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        cv2.imshow("grey", self.grey)

        #if self.count > 20:
            #self.out.write(self.r_frame)

