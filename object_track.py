import cv2
import numpy as np
import time
import argparse

# cd Documents \r cd OpenCV_Scripts \r python object_track.py

px_cols = 640
px_rows = 480


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--cam", required=True,
	help="Camera Index (from 0 to number of connected webcams)")
args = vars(ap.parse_args())

def denoise(frame):
    frame = cv2.medianBlur(frame, 5)
    frame = cv2.GaussianBlur(frame, (5, 5), 0)
    return frame

def checkArea(area, lower, upper):
    if area > lower and area < upper:
        return 1
    else:
        return 0

#Upper & lower bounds for general colours
g_lowerBound = np.array([34,100,40])
g_upperBound = np.array([100,255,255])
y_lowerBound = np.array([13,20,60])
y_upperBound = np.array([20,255,255])
r_lowerBound = np.array([0,140,200])
r_upperBound = np.array([17, 255,255])
b_lowerBound = np.array([95,60,80])
b_upperBound = np.array([130, 255, 255])

#HSV Bounds Arrays for LEDs
g_led_lower = np.array([32,46,207])
g_led_upper = np.array([59,255,255])
y_led_lower = np.array([19,0,216])
y_led_upper = np.array([28,255,255])
r_led_lower = np.array([0,0,216])
r_led_upper = np.array([5, 255,255])

found_blue = 0
found_green = 0
found_red = 0

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))
#print str(args["cam"])
cam = int(args["cam"])
cap = cv2.VideoCapture(cam)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("output.avi", fourcc, 10.0, (px_cols,px_rows))

count = 0
b_area_list = []
g_area_list = []
r_area_list = []
#ont =cv2.cv.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX,2,0.5,0,3,1)
font = cv2.FONT_HERSHEY_COMPLEX
r,f = cap.read()
while True:
    ret, frame = cap.read()
    #Resized to process faster
    frame = cv2.resize(frame,(720,540))
    r_frame = cv2.resize(frame,(px_cols, px_rows))
    #r_frame1 = cv2.resize(frame,(340,220))
    denoise(r_frame)
    #denoise(r_frame1)
    frame_HSV = cv2.cvtColor(r_frame,cv2.COLOR_BGR2HSV)


    # Create filter for yellow colour
    y_mask = cv2.inRange(frame_HSV, y_lowerBound, y_upperBound)
    y_maskOpen=cv2.morphologyEx(y_mask,cv2.MORPH_OPEN,kernelOpen)
    y_maskClose=cv2.morphologyEx(y_maskOpen,cv2.MORPH_CLOSE,kernelClose)
    y_maskFinal = y_maskClose

    # Create filter for red colour
    r_mask = cv2.inRange(frame_HSV, r_lowerBound, r_upperBound)
    r_maskOpen = cv2.morphologyEx(r_mask, cv2.MORPH_OPEN, kernelOpen)
    r_maskClose = cv2.morphologyEx(r_maskOpen, cv2.MORPH_CLOSE, kernelClose)
    r_maskFinal = denoise(r_maskClose)

    # Create filter for green colour
    g_mask = cv2.inRange(frame_HSV, g_lowerBound, g_upperBound)
    g_maskOpen = cv2.morphologyEx(g_mask, cv2.MORPH_OPEN, kernelOpen)
    g_maskClose = cv2.morphologyEx(g_maskOpen, cv2.MORPH_CLOSE, kernelClose)
    g_maskFinal = denoise(g_maskClose)
    g_maskFinal = denoise(g_maskClose)

    # Create filter for green colour
    b_mask = cv2.inRange(frame_HSV, b_lowerBound, b_upperBound)
    b_maskOpen = cv2.morphologyEx(b_mask, cv2.MORPH_OPEN, kernelOpen)
    b_maskClose = cv2.morphologyEx(b_maskOpen, cv2.MORPH_CLOSE, kernelClose)
    b_maskFinal = denoise(b_maskClose)
    b_maskFinal = denoise(b_maskFinal)

    #Find contours in the red & yellow masks
    y_im,y_contours,hier = cv2.findContours(y_maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    r_im, r_contours, r_hier = cv2.findContours(r_maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    g_im, g_contours, g_hier = cv2.findContours(g_maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    b_im, b_contours, b_hier = cv2.findContours(b_maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours = [b_contours, g_contours, r_contours]

    # Iterate through contours for each colour & draw a box round a sufficient cluster.
    cnt_areas = []

    for i in range(len(contours)):
        if i == 0:
            cv2.drawContours(r_frame,contours[i],-1,(255, 0, 0),3)
        elif i == 1:
            cv2.drawContours(r_frame, contours[i], -1, (0, 255, 0), 3)
        else:
            cv2.drawContours(r_frame, contours[i], -1, (0, 0, 255), 3)
        #cv2.drawContours(frame_HSV, contours[i], -1, (0, 255, 255), 3)
        for j in range(len(contours[i])):
            x, y, w, h = cv2.boundingRect(contours[i][j])
            if i == 0:
                #print "Blue Height: %s\n Blue Width: %s" % (h,w)
                # The colour blue
                colour = (255,0,0)
                cv2.circle(r_frame, (x, y), 2, colour, 1)
                # The area of the blue object contour in rows * cols
                b_area = cv2.contourArea(contours[i][j])
                # Function checks area's within bounds

                if checkArea(b_area, 100, 500):
                    #Draws a rectangle around the contour bounds
                    cv2.rectangle(r_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    print "Co-ords: ", (x,y)

                print "Blue Area: ", b_area
                if b_area > 40 and count > 3 and len(b_area_list) < 3 :
                    b_area_list.append(b_area)
                elif b_area > 40 and len(b_area_list) > 2:
                    b_area_list.append(b_area)
                    b_len = len(b_area_list)
                    if (b_area_list[b_len-2] + b_area_list[b_len-1])/2 > 40:
                        if checkArea(b_area, 40, 1000):
                            #print "Blue Object Found"
                            found_blue +=1

            elif i == 1:

                g_area = cv2.contourArea(contours[i][j])
                #print "Green Height: %s\n Green Width: %s" % (h, w)
                colour = (0, 255, 0)
                cv2.circle(r_frame, (x, y), 2, colour, 2)
                if checkArea(g_area, 100, 500):
                    cv2.rectangle(r_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print "Green Area: ", g_area
                if g_area > 40 and count > 3 and len(g_area_list) < 3 :
                    g_area_list.append(g_area)
                elif g_area > 40 and len(g_area_list) > 2:
                    g_area_list.append(g_area)
                    g_len = len(g_area_list)
                    if (g_area_list[g_len - 2] + g_area_list[g_len - 1]) / 2 > 40:
                        #print "Green Object Found"
                        found_green += 1
            else:
                cv2.circle(r_frame, (x+w, y+h), 2, (0, 0, 255), 4)
                r_area = cv2.contourArea(contours[i][j])
                colour = (0,0,255)
                if checkArea(r_area, 100,500):
                    cv2.rectangle(r_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                print "Red Area:", r_area
                if r_area > 40 and count > 3 and len(r_area_list) < 3 :
                    r_area_list.append(r_area)

                elif r_area > 40 and len(r_area_list) > 2:
                    r_area_list.append(r_area)
                    r_len = len(r_area_list)
                    if (r_area_list[r_len - 2] + r_area_list[r_len - 1]) / 2 > 40:
                        if checkArea(r_area, 100, 1000):
                            #print "Red Object Found"
                            found_red += 1

            # Write the contour rectangle index in subscript of the rectangle
            #cv2.putText(r_frame, str(j + 1), (x-10, y+h+10), font, fontScale = 0.75, color =  colour, thickness = 2)
            cv2.putText(r_frame, "%s, %s" %(str(x),str(y)), (x-20, y + h+20
                                                             ), font, fontScale=0.5, color=colour, thickness=2)

    #print len(x_list), len(y_list)
    for px in range(px_cols/40):
        cv2.line(r_frame, ((px*40),0), ((px*40),7), thickness= 1, color= (0,0,0))
        cv2.putText(r_frame, str(px*40), ((px* 40), 25), color= (0,0,0), thickness=1, fontScale= 1, fontFace=cv2.FONT_HERSHEY_PLAIN)
    # Show all the windows
    cv2.imshow("Blue Mask", b_maskClose)
    cv2.imshow("Red Mask", r_maskClose)
    cv2.imshow("Green Mask", g_maskClose)
    cv2.imshow("Contoured Frame", r_frame)
    if count > 20:
        out.write(r_frame)
    #print "Red Count: ", found_red
    print "Green Count: ",found_green
    #print "Blue Count: ",found_blue

    count += 1
    print "\n ----%s----- \n" % str(count)
    k = cv2.waitKey(10) & 0xFF
    if k == 27:
        break

    time.sleep(0.2)

