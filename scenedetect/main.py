import sys
import time

import cv2
import numpy as np


def scenedetect(cap, threshold=30):
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    downscale_factor = int(w / 200)
    last_hsv = None
    first = 0
    curr = 0

    while True:
        ret, im = cap.read()
        if not ret:
            break

        curr_hsv = im[::downscale_factor, ::downscale_factor]
        curr_hsv = cv2.cvtColor(curr_hsv, cv2.COLOR_BGR2HSV)
        curr_hsv = curr_hsv.astype('int32')
        if last_hsv is not None:
            delta_hsv = np.mean(np.abs(curr_hsv - last_hsv))
            if delta_hsv >= threshold:
                yield first, curr, delta_hsv
                first = curr

        last_hsv = curr_hsv
        curr += 1


fn = 'video.rmvb'
cap = cv2.VideoCapture(fn)
start = time.time()
for first, last, delta_hsv in scenedetect(cap):
    print(first, last, delta_hsv)
print(time.time() - start)
cap.release()
