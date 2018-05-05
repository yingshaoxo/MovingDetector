# coding:utf8
import cv2
import sys
import numpy as np

class MovingDetector():
    def __init__(self, device):
        self.camera = cv2.VideoCapture(device)

        if not self.camera.isOpened():
            print("Could not open camera")
            sys.exit()

    def detect(self):
        history = 10#20    # 训练帧数

        bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)  # 背景减除器，设置阴影检测
        #bs = cv2.createBackgroundSubtractorKNN(detectShadows=True)
        bs.setHistory(history)

        frames = 0

        while True:
            res, frame = self.camera.read()

            if not res:
                break

            fg_mask = bs.apply(frame)   # 获取 foreground mask

            if frames < history:
                frames += 1
                continue

            # 对原始帧进行膨胀去噪
            th = cv2.threshold(fg_mask.copy(), 244, 255, cv2.THRESH_BINARY)[1]
            th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
            dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 3)), iterations=2)
            # 获取所有检测框
            image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
 
            if len(contours) != 0:
                # find the biggest area
                c = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(c)
                print(x, y, w, h)
                print("center point is:", int((x+w)/2), int((y+h)/2))
                print("\n")
                # shrink area
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                # convert all coordinates floating point values to int
                box = np.int0(box)
                # draw a red 'nghien' rectangle
                cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)

            cv2.imshow("detection", frame)
            cv2.imshow("back", dilated)

            if cv2.waitKey(110) & 0xff == 27:
                break

if __name__ == '__main__':
    detector = MovingDetector(0)
    detector.detect() 
