import queue
import threading
import time

import numpy as np


class data_to_frame(threading.Thread):
    def __init__(self, input_cache, frame_size=(400, 400)):
        threading.Thread.__init__(self)
        # the input cache is the output buffer of the previous stage
        self.input_cache = input_cache
        self.output_cache = queue.Queue()
        self.frame_size = frame_size
        self.active = False
        # self.head_size = 6 # size of the header "<cpkg>"
        # self.tail_size = 7 # </cpkg>
    def _conver_data_to_frame(self):
        if not self.input_cache.empty():
            new_frame = np.empty(self.frame_size, np.uint8)
            incoming_data = self.input_cache.get()
            col = self.frame_size[0]
            row = self.frame_size[1]
            try:
                for i, d in enumerate(incoming_data):
                    new_frame[i // col][i % col] = d
            except Exception as e:
                print(incoming_data)
                print(len(incoming_data))
                print(i,d)
                print(e)
                return
            # print(new_frame)
            self.output_cache.put(new_frame)

    def run(self) -> None:
        self.active = True
        while self.active:
            self._conver_data_to_frame()
            time.sleep(0.000001)

    def stop(self):
        self.active = False

def test_data_to_frame():
    i = queue.Queue()
    i.put(b'\x33\x66\x88\x99\x33\x66\x88\x99\x33\x66\x88\x99\x33\x66\x88\x99')
    d = data_to_frame(i, (4, 4))
    d._conver_data_to_frame()


if __name__ == '__main__':
    test_data_to_frame()
