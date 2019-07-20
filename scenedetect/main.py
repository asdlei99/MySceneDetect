import sys
import time

import cv2
import numpy as np


def scenedetect(cap, threshold=30):
    w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    downscale_factor = int(w / 200)
    last_hsv = None
    first = None
    i = 0

    while True:
        ret, im = cap.read()
        if not ret:
            break

        curr_hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV).astype('int32')
        curr_hsv = curr_hsv[::downscale_factor, ::downscale_factor]
        if first is None:
            first = i
        else:
            delta_hsv = np.mean(np.abs(curr_hsv - last_hsv))
            if delta_hsv >= threshold:
                yield first, i, delta_hsv
                first = None

        last_hsv = curr_hsv
        i += 1


fn = 'video.rmvb'
cap = cv2.VideoCapture(fn)
start = time.time()
for first, last, delta_hsv in scenedetect(cap):
    print(first, last, delta_hsv)
    sys.stdout.flush()
print(time.time() - start)
cap.release()
PySceneDetect
