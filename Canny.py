import cv2
import numpy as np
import time
import pytesseract as tess
from PIL import Image

def auto_canny(image, lower = 100, upper = 180):
    filtered = cv2.adaptiveThreshold(image.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15,3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    or_image = cv2.bitwise_or(image, closing)
    edged = cv2.Canny(or_image, lower, upper)
    # return the edged image
    return or_image

img = cv2.imread("pic15.jpg",0)
start = time.time()
while(1):
    fin = auto_canny(img)
    cv2.imshow("canny",fin)
    cv2.imshow("original", (img))
    key = cv2.waitKey(10) & 0xFF
    print tess.image_to_string(Image.fromarray(fin)).encode("utf-8")
    if key==27:
        break
    if abs(time.time() - start) > 20:
        break
cv2.destroyAllWindows()

