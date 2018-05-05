import numpy as np
import cv2

cap = cv2.VideoCapture(0)
ret, last_frame = cap.read()

if last_frame is None:
    exit()

while(cap.isOpened()):
    ret, frame = cap.read()

    if frame is None:
        break

    diff = cv2.absdiff(last_frame, frame)
    diff = cv2.bitwise_not(diff)

    cv2.imshow('frame', frame)
    cv2.imshow('diff_frame', diff)

    last_frame = frame

    if cv2.waitKey(27) >= 0:
        break

cap.release()
cv2.destroyAllWindows()
