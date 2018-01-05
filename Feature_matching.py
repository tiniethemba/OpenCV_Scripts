import numpy as np
import cv2

class FeatureMatching:
    def __init__(self):
        self.min_hessian = 400
        self.SURF = cv2.xfeatures2d.SURF_create(self.min_hessian)
        key_query, desc_query = self.SURF.detectAndCompute(img_query, None)