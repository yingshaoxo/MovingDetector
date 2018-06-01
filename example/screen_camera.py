import numpy as np
import pyscreenshot as ImageGrab
import pyautogui
import cv2
import time

box_size = 300//2


def main():
    for i in list(range(3))[::-1]:
        print(i+1)
        time.sleep(1)

    while True:
        pos = pyautogui.position()
        frame = np.array(ImageGrab.grab(
            bbox=(pos[0]-box_size, pos[1]-box_size, pos[0]+box_size, pos[1]+box_size)))
        cv2.imshow('window', cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if cv2.waitKey(110) & 0xFF == 27:
            cv2.destroyAllWindows()
            break


main()
