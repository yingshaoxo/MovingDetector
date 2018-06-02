import numpy as np
import pyscreenshot as ImageGrab
import pyautogui
import cv2


class VideoCamera(object):
    def __init__(self):
        self.screen_width = pyautogui.size()[0]
        self.screen_height = pyautogui.size()[1]

        self.top_left = (self.screen_width//2, 0)
        self.lower_right = (self.screen_width, self.screen_height//2)
        # self.top_left = (0, 0)
        # self.lower_right = (self.screen_width, self.screen_height)

    def get_frame(self):
        frame = np.array(ImageGrab.grab(bbox=(
            self.top_left[0], self.top_left[1], self.lower_right[0], self.lower_right[1])))
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
