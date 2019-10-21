# Copyright (C) 2015 Ross D Milligan
# GNU GENERAL PUBLIC LICENSE Version 3 (full notice can be found at https://github.com/rdmilligan/SaltwashAR)

import cv2
from threading import Thread
from time import sleep
import urllib.request
import numpy as np

class Webcam:

    def __init__(self):
        #self.video_capture = cv2.VideoCapture(0)
        #self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        #self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
        self.current_frame = None #self.video_capture.read()[1]
        self.last_state = False
        self.need_update = False
        self.ip = ""

    # create thread for capturing images
    def start(self, ip):
        self.ip = ip
        Thread(target=self._update_frame, args=()).start()

    def _update_frame(self):
        while True:
            try:
                URL = "http://" + self.ip + ":8080/shot.jpg"
                img_arr = np.array(bytearray(urllib.request.urlopen(URL).read()),dtype=np.uint8)
                img = cv2.imdecode(img_arr,-1)
                if (len(img) == 0):
                    print("len == 0")
                    continue
                self.need_update = False
                self.last_state = True
                self.current_frame = img
            except e:
                print(e)
                continue
            # cv2.imgshow('asd', img)

        #while(True):
        #    if (not self.need_update):
        #        sleep(0.1)
        #        continue
        #    self.need_update = False
        #    ret, frame = self.video_capture.read()
        #    self.last_state = ret
        #    self.current_frame = frame

    # get the current frame
    def get_current_frame(self):
        self.need_update = True
        return self.current_frame

    # get the current frame
    def get_current_state(self):
        tmp = self.last_state
        self.last_state = False
        return tmp
