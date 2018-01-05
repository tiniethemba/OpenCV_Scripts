# generate_descriptors.py
import cv2
import numpy as np
from os import walk
from os.path import join
import sys

class Descriptor:
        def __init__(self, folder):
            self.folder = folder
            files = []
            for (dirpath, dirnames, filenames) in walk(folder):
                files.extend(filenames)
            for f in files:
                if ".npy" not in f:
                    self.save_descriptor(folder, f, cv2.xfeatures2d.SIFT_create())
        def save_descriptor(self, folder, image_path, feature_detector):
            img = cv2.imread(join(folder, image_path), 0)
            keypoints, descriptors = feature_detector.detectAndCompute(img,
            None)
            descriptor_file = image_path.replace("jpg", "npy")

            np.save(join(folder, descriptor_file), descriptors)
if __name__ == "__main__":
    the_dir = sys.argv[1]
    x = Descriptor(the_dir)