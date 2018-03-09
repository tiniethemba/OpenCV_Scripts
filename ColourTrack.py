import cv2
import numpy as np
import talker

class ColourTrack():
    def __init__(self, px_cols, px_rows, cam = None, redBounds=None, greenBounds=None, blueBounds=None, yellowBounds = None, whiteBounds = None, filename = None):

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
        self.objects = {
        }
        self.co_ord_list = []
        self.features_count = 0
        if redBounds == None:
            self.red = 0
        else:
            self.red = 1
            self.r_lowerBound = redBounds[0]
            self.r_upperBound = redBounds[1]
        if greenBounds == None:
            self.green = 0
        else:
            self.green = 1
            self.g_lowerBound = greenBounds[0]
            self.g_upperBound = greenBounds[1]
        if blueBounds == None:
            self.blue = 0
        else:
            self.blue = 1
            self.b_lowerBound = blueBounds[0]
            self.b_upperBound = blueBounds[1]
        if yellowBounds == None:
            self.yellow = 0
        else:
            self.yellow = 1
            self.y_lowerBound = yellowBounds[0]
            self.y_upperBound = yellowBounds[1]
        if whiteBounds == None:
            self.white = 0
        else:
            self.white = 1
            self.w_lowerBound = whiteBounds[0]
            self.w_upperBound = whiteBounds[1]
        if cam:
            self.ret, self.frame = self.cap.read()
        else:
            self.frame = cv2.imread(filename)



        # Resized to process faster
        self.frame = cv2.resize(self.frame, (self.px_cols, self.px_rows))
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
            cv2.imshow("Open", self.y_maskOpen)
            cv2.imshow("CLosed", self.y_maskClose)

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
        if self.blue:
            b_ret, b_thresh = cv2.threshold(self.b_maskFinal.copy(), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            b_im, self.b_contours, b_hier = cv2.findContours(b_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            self.b_contours = None
        if self.green:
            g_ret, g_thresh = cv2.threshold(self.g_maskFinal.copy(), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            g_im, self.g_contours, g_hier = cv2.findContours(g_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        else:
            self.g_contours = None
        if self.red:
            r_ret, r_thresh = cv2.threshold(self.r_maskFinal.copy(), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            r_im, self.r_contours, r_hier = cv2.findContours(r_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        else: self.r_contours = None
        if self.yellow:
            y_ret, y_thresh = cv2.threshold(self.y_maskFinal.copy(), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            y_im, self.y_contours, y_hier = cv2.findContours(y_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        else:
            self.y_contours = None
        if self.white:
            w_ret, w_thresh = cv2.threshold(self.w_maskFinal.copy(), 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            w_im, self.w_contours, w_hier = cv2.findContours(w_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else: self.w_contours = None
        self.contours = [self.b_contours, self.g_contours, self.r_contours, self.y_contours, self.w_contours]

    def drawFrame(self, resize = 1):
        self.shapes = []
        # Iterate through contours for each colour & draw a box round a sufficient cluster.
        for i in range(len(self.contours)):

            if i == 0:
                colors = (255,0,0) # blue
                self.colour_string = "Blue"
                cv2.drawContours(self.r_frame, self.contours[i], -1, colors, 3)
            elif i == 1:
                colors = (0,255,0) # green
                self.colour_string = "Green"
                cv2.drawContours(self.r_frame, self.contours[i], -1, colors, 3)
            elif i == 2:
                self.colour_string = "Red"
                colors = (0,0,255) # red
                cv2.drawContours(self.r_frame, self.contours[i], -1, colors, 3)
            elif i == 3:
                self.colour_string = "Yellow"
                colors = (0,255,255) # yellow
                cv2.drawContours(self.r_frame, self.contours[i], -1, colors, 3)
            elif i == 4:
                self.colour_string = "White"
                colors = (255,255,255) # white
                cv2.drawContours(self.r_frame, self.contours[i], -1, colors, 3)
            the_area = 0
            #print "%s: Contours List Length: %d" % (self.colour_string, len(self.contours[i]))
            if self.contours[i] is not None:
                for j in range(len(self.contours[i])):
                    gen_area = cv2.contourArea(self.contours[i][j])
                    if self.checkArea(gen_area, resize * self.frame_area/10000, resize * self.frame_area):
                        cv2.imshow("Pre-shape frame", self.r_frame)
                        rect = cv2.minAreaRect(self.contours[i][j])
                        box = cv2.boxPoints(rect)
                        self.box = np.int0(box)
                        #cv2.drawContours(self.r_frame,[self.box],0,colors,2)
                        epsilon = 0.001 * cv2.arcLength(self.contours[i][j], True)
                        approx = cv2.approxPolyDP(self.contours[i][j], epsilon, True)
                        #hull = cv2.convexHull(self.contours[i][j])
                        cv2.drawContours(self.r_frame,[approx],0,colors,3)

                        if i == 0:
                            self.b_area = cv2.contourArea(self.contours[i][j])
                            the_area = int(self.b_area)
                        elif i == 1:
                            self.g_area = cv2.contourArea(self.contours[i][j])
                            the_area = int(self.g_area)
                        elif i == 2:
                            self.r_area = cv2.contourArea(self.contours[i][j])
                            the_area = int(self.r_area)
                        elif i == 3:
                            self.y_area = cv2.contourArea(self.contours[i][j])
                            the_area = int(self.y_area)
                        elif i == 4:
                            self.w_area = cv2.contourArea(self.contours[i][j])
                            the_area = int(self.w_area)
                        else:
                            print "Oh Oh, spaghetti-o's!!"

                        x1,y1 = box[0]
                        x2,y2 = box[1]
                        x3,y3 = box[2]
                        x4,y4 = box[3]
                        x1 = int(x1)
                        x2 = int(x2)
                        x3 = int(x3)
                        x4 = int(x4)
                        y1 = int(y1)
                        y2 = int(y2)
                        y3 = int(y3)
                        y4 = int(y4)
                        co_ords = (x2,y2)
                        #print "APPROXIMATION LENGTH %d "%len(approx)
                        appr_list = []
                        count = 0
                        l_approx = np.array(approx).tolist()
                        for appr in l_approx:
                            for app in appr:
                                appr_list.append(app)

                        self.co_ord_list.append(co_ords)
                        self.box_co_ords = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
                        #print "BOX CO-ORDINATES %s" % str(approx)
                        self.shapes.append(self.shape(self.contours[i][j], self.r_frame, colors))
                        current_shape = self.shape(self.contours[i][j], self.r_frame, colors)
                        self.features(co_ords,self.box_co_ords, appr_list, self.colour_string, current_shape, area=the_area)
                        # Function checks area's within bounds, and draws a rectangle around the contour bounds.


                        # Write the contour rectangle index in subscript of the rectangle
                        if self.checkArea(the_area, resize * self.frame_area/(10000), resize * self.frame_area):
                            cv2.putText(self.r_frame, "[%s]: %s, %s, %s" % (self.objects[str(co_ords)]['type'],str(x2), str(y2), str(the_area)), (x2, y2), self.font, fontScale=0.5, color=colors, thickness=2)

        #cv2.imshow("White Mask", self.r_maskClose)
        self.r_frame = cv2.resize(self.r_frame,dsize = (0,0), fx = resize, fy= resize)
        cv2.imshow("Contoured Frame", self.r_frame)

    # FUnction to determine the shape of contours on the contoured frame
    def shape(self, c, frame = None, colour=None):
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(approx) == 3:
            shape = "triangle"

        # if the shape has 4 vertices, it is either a square or
        # a rectangle
        elif len(approx) == 4 :
            # compute the bounding box of the contour and use the
            # bounding box to compute the aspect ratio
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)

            # a square will have an aspect ratio that is approximately
            # equal to one, otherwise, the shape is a rectangle
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        # if the shape is a pentagon, it will have 5 vertices
        elif len(approx) == 5:
            shape = "rectangular"

        # otherwise, we assume the shape is a circle
        else:
            shape = "circle"

        M = cv2.moments(c)
        self.cX = int(M["m10"] / M["m00"])
        self.cY = int(M["m01"] / M["m00"])

        # Draw the contour and center of the shape on the image

        # Draw centre circle on shape
        cv2.circle(frame, (self.cX, self.cY), 7, colour, -1)
        cv2.putText(frame, "%s" % shape, (self.cX - 20, self.cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, colour, 2)

        return shape

    # Function to publish the feature/obstacle information from the frame to a ROS node.
    def ROS_pub(self, message = None, topic = None, rate = None):
        talk = talker.Talker(message,topic,rate)
        if message !=  None:
            talk.talker()

    def auto_canny(self, image, lower=100, upper=180):
        filtered = cv2.adaptiveThreshold(image.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 3)
        kernel = np.ones((1, 1), np.uint8)
        opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
        or_image = cv2.bitwise_or(image, closing)
        # edged = cv2.Canny(or_image, lower, upper)
        # return the edged image
        return or_image


    # Function applying logic to contour properties to categorise the obstacles
    def features(self, co_ords, box_co_ords, approx, colour, shape, area = None):
        #self.features_count += 1
        c = str(co_ords)
        self.objects[c] = {}
        self.objects[c]['co-ords'] = box_co_ords
        #print "\n\n\n"
        #approx = approx.split("\n\n")
        #approx = ",".join(approx)
        self.objects[c]['str_coords'] = "%s" %(str(approx))
        self.objects[c]['colour'] = colour
        self.objects[c]['shape'] = shape
        self.objects[c]['area'] = area
        self.objects[c]['centre'] = (self.cX, self.cY)

        #print "\n %s, %s, %s " % (c,self.objects[c]['colour'],self.objects[c]['shape'])


        if shape == 'rectangular' and colour != 'White':
            self.objects[c]['type'] = "Potential Robot"

        elif shape == 'circle' and colour == "Red":
            self.objects[c]['type'] = "Fuel Cell"
            print "FOUND FUEL CELL!!!!!!"

        elif shape == 'rectangle' and colour == "Green":
            self.objects[c]['type'] = "DaNI Robot"


        elif shape == 'rectangle' and colour == "Blue":
            self.objects[c]['type'] = "Chair"

        elif colour == "Yellow":
            self.objects[c]['type'] = "Potential Marker"

        elif shape == 'rectangle' and colour == "Red":
            self.objects[c]['type'] = "Tri-Track"

        elif colour == "White":
            self.objects[c]['type'] = "Terrain edge"

        else:
            self.objects[c]['type'] = "Unknown"
            print "ERROR: CAN'T IDENTIFY THE TERRAIN FEATURE"


    def findBridge(self):
        white_rect = []
        wr_count = 0
        x_ok = "NOT OK"
        x_list = []
        y_list = []
        for co_ord in self.co_ord_list:
            c = str(co_ord)
            type = self.objects[c]['type']
            shape = self.objects[c]['shape']
            area = self.objects[c]['area']
            if type == "Terrain edge" and shape == "rectangle" and area > self.frame_area/1000:
                white_rect.append(self.objects[c])
                x_list.append(self.objects[c]['centre'][0])
                y_list.append(self.objects[c]['centre'][1])
        print "\n\nWhite rect %s" %str(white_rect)
        for wr in white_rect:
            x = wr['centre'][0]
            y = wr['centre'][1]
            for i in range(len(white_rect)):
                if x_list[i] + self.px_cols/2 > x  and x_list[i] - self.px_cols/2 < x and x != x_list[i]:
                    x_ok = "OK"
                if y_list[i] + self.px_rows/20 > y  and y_list[i] - self.px_rows/20 < y and y != y_list[i]:
                    if x_ok == "OK":
                        print "FOUND BRIDGE"




    def saveFrame(self, normal_frame_name ,contour_frame_name):
        cv2.imwrite(normal_frame_name,self.frame)
        cv2.imwrite(contour_frame_name, self.r_frame)


