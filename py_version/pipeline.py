import threading
import time

import commu
import Display
import numpy as np

import data_to_frame
import parser


class pipeline(threading.Thread):
    def __init__(self, receiver=commu.receiver(), monitor=None):
        threading.Thread.__init__(self)
        self.receiver = receiver
        if monitor is None:
            monitor = Display.Display(img=np.zeros((400,400), np.uint8), real_time=True)
        self.monitor = monitor
        self.active = False
        self.tcp_parser = parser.tcp_parser()
        self.data_frame_converter = data_to_frame.data_to_frame(input_cache=self.tcp_parser.outputCache, frame_size=(400,400))
    def stop(self):
        self.active = False
        print("ppl to stop")

    def run(self) -> None:
        self.receiver.start()
        self.monitor.start()
        self.active = True
        self.tcp_parser.start()
        self.data_frame_converter.start()


        while self.active:
            data = self.receiver.get_client_message()
            if data:
                self.tcp_parser.feed(data)
            if not self.data_frame_converter.output_cache.empty():
                self.monitor.update(self.data_frame_converter.output_cache.get())

        self.receiver.stop()
        self.tcp_parser.stop()
        self.data_frame_converter.stop()
        self.monitor.stop()
        print("ppl stopped")
    def __del__(self):
        self.receiver.__del__()
        self.tcp_parser.__del__()


if __name__ == '__main__':
    p = pipeline()
    p.start()

    try:
        while True:
            time.sleep(0.000001)
    except Exception as e:
        print(e)
    finally:
        p.stop()
        p.__del__()
