import threading
import time
import numpy as np
import cv2
from Display import Display

n_img = np.zeros([400, 400])

a = Display(img=n_img, real_time=False, size=(400,400))
a.start()


for i in range(100):
    # for c,x in enumerate(n_img):
        # for cc,y in enumerate(x):
            # n_img[c][cc] = 1/(i % 255 + 1)
    time.sleep(0.01)
    a.update(n_img+0.8)

a.stop()
