from os.path import join
from os import walk
import numpy as np
import cv2
from sys import argv

# create an array of filenames
folder = argv[1]
# The image to be compared against
query = cv2.imread( "tri_track.jpg", 0)

# create files, images, descriptors globals
files = []
images = []
descriptors = []
for (dirpath, dirnames, filenames) in walk(folder):
    files.extend(filenames)
    for f in files:
        if f.endswith("npy") and f != "tri_track.npy":
            descriptors.append(f)
    print "Descriptors", descriptors

# create the sift detector
sift = cv2.xfeatures2d.SIFT_create()
query_kp, query_ds = sift.detectAndCompute(query, None)

# create FLANN matcher
FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)
flann = cv2.FlannBasedMatcher(index_params, search_params)


# minimum number of matches
MIN_MATCH_COUNT = 30
potential_culprits = {}
print ">> Initiating picture scan..."
lead_suspect = []
for d in descriptors:
    print "--------- analyzing %s for matches ------------" % d
    matches = flann.knnMatch(query_ds, np.load(join(folder, d)), k=2)
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)
    if len(good) > MIN_MATCH_COUNT:
        print "%s is a match! (%d)" % (d, len(good))
        lead_suspect.append(d)
    else:
        print "%s is not a match" % d
        potential_culprits[d] = len(good)
    #b = cv2.drawMatches()
max_matches = None
potential_suspect = None
print potential_culprits
for culprit, matches in potential_culprits.iteritems():
    if max_matches == None or matches > max_matches:
        max_matches = matches
        potential_suspect = culprit
print "Leading suspect is %s" % lead_suspect[0].replace("npy","").upper()
print "potential suspect is %s" % potential_suspect.replace("npy","").upper()