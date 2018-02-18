import cv2
import numpy as np

class ColourTrack():
    def __init__(self, cam, px_cols, px_rows, redBounds, greenBounds, blueBounds, yellowBounds = None, whiteBounds = None, video_mode = 0, filename = None):
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
        self.frame_area = self.px_cols * self.px_rows
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
        if video_mode == True:
            self.ret, self.frame = self.cap.read()
        else:
            self.frame = cv2.imread(filename)
            self.cap.release()


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
            self.r_maskFinal = self.denoise(self.r_maskFinal)

        if self.green:
        # Create filter for green colour
            self.g_mask = cv2.inRange(self.frame_HSV, self.g_lowerBound, self.g_upperBound)
            self.g_maskOpen = cv2.morphologyEx(self.g_mask, cv2.MORPH_OPEN, self.kernelOpen)
            self.g_maskClose = cv2.morphologyEx(self.g_maskOpen, cv2.MORPH_CLOSE, self.kernelClose)
            self.g_maskFinal = self.denoise(self.g_maskClose)
            self.g_maskFinal = self.denoise(self.g_maskFinal)


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
            #self.y_maskFinal = self.denoise(self.y_maskFinal)

        if self.white:
            # Create filter for yellow colour
            self.w_mask = cv2.inRange(self.frame_HSV, self.w_lowerBound, self.w_upperBound)
            self.w_maskOpen = cv2.morphologyEx(self.w_mask, cv2.MORPH_OPEN, self.kernelOpen)
            self.w_maskClose = cv2.morphologyEx(self.w_maskOpen, cv2.MORPH_CLOSE, self.kernelClose)
            self.w_maskFinal = self.denoise(self.w_maskClose)
            self.w_maskFinal = self.denoise(self.w_maskFinal)

    def adaptive(self, frame_grey):
        grey = cv2.adaptiveThreshold(frame_grey, 155, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        bgr = cv2.cvtColor(grey, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        return hsv

    def makeContours(self):

        # Find contours in the red & yellow masks

        b_ret, b_thresh = cv2.threshold(self.b_maskFinal.copy(), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        b_im, self.b_contours, b_hier = cv2.findContours(b_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        g_ret, g_thresh = cv2.threshold(self.g_maskFinal.copy(), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        g_im, self.g_contours, g_hier = cv2.findContours(g_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        r_ret, r_thresh = cv2.threshold(self.r_maskFinal.copy(), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        r_im, self.r_contours, r_hier = cv2.findContours(r_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        y_ret, y_thresh = cv2.threshold(self.y_maskFinal.copy(), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        y_im, self.y_contours, y_hier = cv2.findContours(y_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        w_ret, w_thresh = cv2.threshold(self.w_maskFinal.copy(), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        w_im, self.w_contours, w_hier = cv2.findContours(w_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        self.contours = [self.b_contours, self.g_contours, self.r_contours, self.y_contours, self.w_contours]

    def drawFrame(self):
        self.shapes = []
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
            the_area = 0
            for j in range(len(self.contours[i])):
                gen_area = cv2.contourArea(self.contours[i][j])
                if self.checkArea(gen_area, self.frame_area/(10**4), self.frame_area):
                    self.shapes.append(self.shape(self.contours[i][j], self.r_frame, colors))
                    x, y, w, h = cv2.boundingRect(self.contours[i][j])
                    if i == 0:
                        self.colour_string = "Blue"
                        self.b_area = cv2.contourArea(self.contours[i][j])
                        the_area = self.b_area
                    elif i == 1:
                        self.g_area = cv2.contourArea(self.contours[i][j])
                        self.colour_string = "Green"
                        the_area = self.g_area
                    elif i == 2:
                        self.colour_string = "Red"
                        self.r_area = cv2.contourArea(self.contours[i][j])
                        the_area = self.r_area
                    elif i == 3:
                        self.colour_string = "Yellow"
                        self.y_area = cv2.contourArea(self.contours[i][j])
                        the_area = self.y_area
                    elif i == 4:
                        self.colour_string = "White"
                        self.w_area = cv2.contourArea(self.contours[i][j])
                        the_area = self.w_area
                    else:
                        print "Oh Oh, spaghetti-o's!!"
                    cv2.circle(self.r_frame, (x, y), 2, colors, 1)  # global
                    # Function checks area's within bounds, and draws a rectangle around the contour bounds.
                    if self.checkArea(the_area, 1000, 5000):
                        cv2.rectangle(self.r_frame, (x, y), (x + w, y + h), colors, 2)
                    print "%s Area: %s" % (self.colour_string, str(the_area))
                    print "Co-ords: ", (x, y)

                    # Write the contour rectangle index in subscript of the rectangle
                    if self.checkArea(the_area, 500, 1000000):
                        cv2.putText(self.r_frame, "%s, %s" % (str(x), str(y)), (x - 40, y + 45
                                                                       ), self.font, fontScale=0.5, color=colors, thickness=2)

            # Show all the windows
        #cv2.imshow("White Mask", self.r_maskClose)
        cv2.imshow("Contoured Frame", self.r_frame)
        #cv2.imshow("grey", self.grey)

    def shape(self, c, frame = None, colour=None):
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4:
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "pentagon"

        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # draw the contour and center of the shape on the image
        cv2.drawContours(frame, [c], -1, colour, 2)
        cv2.circle(frame, (cX, cY), 7, colour, -1)
        cv2.putText(frame, "%s"%shape, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 2)

        return shape

    def auto_canny(self, image, sigma=0.33):
        # compute the median of the single channel pixel intensities
        v = np.median(image)
        # apply automatic Canny edge detection using the computed median
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)
        # return the edged image
        return edged


    def saveFrame(self, normal_frame_name ,contour_frame_name):
        cv2.imwrite(normal_frame_name,self.frame)
        cv2.imwrite(contour_frame_name, self.r_frame)

