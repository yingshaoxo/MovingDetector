import pyscreenshot as ImageGrab
# from PIL import import ImageGrab
import numpy as np
import cv2
import time


Cam_Device = 1
Screen_Width = 800
Screen_Hight = 600
Cam_Width = 320
Cam_Hight = 240
Delay = 0.2


cam = cv2.VideoCapture(Cam_Device)

while(True):
    # capture screen
    screen_img = ImageGrab.grab(bbox=(0, 0, Screen_Width, Screen_Hight))
    img_np = np.array(screen_img)
    screen_img = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)

    # capture camera
    _, cam_img = cam.read()
    cam_img = cv2.resize(cam_img, (Cam_Width, Cam_Hight))
    num_rows, num_cols = cam_img.shape[:2]

    # rotate 90 degree
    rotation_matrix = cv2.getRotationMatrix2D((num_cols/2, num_rows/2), -90, 1)
    cam_img = cv2.warpAffine(cam_img, rotation_matrix, (num_cols, num_rows))

    # horizontal flip
    cam_img = cv2.flip(cam_img, 1)

    # combination
    screen_img[Screen_Hight - Cam_Hight:Screen_Hight,
               Screen_Width - Cam_Width:Screen_Width] = cam_img

    cv2.imshow("test", screen_img)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
    else:
        time.sleep(Delay)
