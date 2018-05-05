import cv2
import numpy as np

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

cam = cv2.VideoCapture(0)

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
origin = cam.read()[1]

while True:
    diff_img = diffImg(t_minus, t, t_plus)
    #diff_img = cv2.bitwise_not(diff_img)
    # 对原始帧进行膨胀去噪
    th = cv2.threshold(diff_img.copy(), 244, 255, cv2.THRESH_BINARY)[1]
    th = cv2.erode(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=2)
    dilated = cv2.dilate(th, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (8, 3)), iterations=2)
    # 获取所有检测框
    image, contours, hier = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        # find the biggest area
        c = max(contours, key=cv2.contourArea) #c = min(contours, key=cv2.contourArea)
        # shrink area
        rect = cv2.minAreaRect(c)
        box = cv2.boxPoints(rect)
        # get center point
        x = int(sum([point[0] for point in box])/4)
        y = int(sum([point[1] for point in box])/4)
        print("the center point is: ({x}, {y})".format(x=x, y=y))
        # convert all coordinates floating point values to int
        box = np.int0(box)
        # draw a red 'nghien' rectangle
        cv2.drawContours(origin, [box], 0, (0, 255, 0), 2)

    cv2.imshow("Movement Indicator", origin)

    # Read next image
    origin = cam.read()[1]
    t_minus = t
    t = t_plus
    t_plus = cv2.cvtColor(origin, cv2.COLOR_RGB2GRAY)

    key = cv2.waitKey(10)
    if key == 27:
        cv2.destroyAllWindows()
        break

print("Goodbye")
