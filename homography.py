import cv2
import numpy as np
import matplotlib.pyplot as plt

img1 = cv2.imread("h.jpg",0)
img2 = cv2.imread("i.jpg",0)

orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img1, None)
kp2, des2 = orb.detectAndCompute(img2,None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

matches = bf.match(des1,des2)
matches = sorted(matches, key = lambda x:x.distance)

print matches
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:100], None, flags = 2)
cv2.imwrite("img3.jpg",img3)
print type(img3)
plt.imshow(img3)
#plt.imshow(img3.reshape(img3.shape[0], img3.shape[1]), cmap=plt.cm.Greys)
plt.show()
