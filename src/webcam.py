# import logging
from cv2 import cv2
from PIL import Image, ImageTk
# from time import gmtime, strftime

class WebCam(object):
    def __init__(self):
        self.vid_source = cv2.VideoCapture(0)

    def get_frame(self):
        if self.vid_source.isOpened():
            _, frame = self.vid_source.read()
            return cv2.imencode('.jpg', frame)[1].tobytes()
        else:
            raise Exception('Unable to open video source')

    def __del__(self):
        if self.vid_source.isOpened():
            self.vid_source.release()