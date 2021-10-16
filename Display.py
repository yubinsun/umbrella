import threading
import time
import cv2


class Display(threading.Thread):

    def __init__(self, img = None, real_time=True, size = (1080,720)):
        """

        :param img: A [[]] of size
        :param real_time: skip frame if a new frame is coming
        :param size: A tuple of size (width, length)
        """
        threading.Thread.__init__(self)
        self.size = size
        self.img = img

        #real_time: skip frame if a new frame is coming
        self.real_time = real_time

        self.updated = threading.Lock()

        self.stop_sig = False

    def run(self) -> None:

        cv2.namedWindow('img', cv2.WINDOW_NORMAL)
        cv2.imshow("img", self.img)
        cv2.waitKey(1)

        l_time = 0
        counter = 0

        while not self.stop_sig:
            self.updated.acquire()
            if self.img is None:
                self.updated.release()
                continue
            cv2.imshow("img", self.img)
            cv2.waitKey(1)
            # stats
            counter += 1
            t = time.time()
            print("frame =" + str(counter) + ", fps = " + str(1 / (t - l_time)))
            l_time = t
            # finalizing
            self.img = None
            self.updated.release()
        print("Quit displaying")

    def stop(self):
        self.stop_sig = True

    def update(self, img:[]):
        while self.real_time and True:
            self.updated.acquire()
            if self.img is None:
                break
        self.updated.acquire()
        self.img = img
        self.updated.release()




