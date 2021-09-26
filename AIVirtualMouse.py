import cv2 as cv
import numpy as np
import HandTrackingModule as htm
import time
from pynput.mouse import Button, Controller

frameR = 100
smoothening = 5

pLocX, pLocY = 0, 0
cLocX, cLoxY = 0, 0

wCam, hCam = 640, 480
wScr, hScr = 1920, 1080

cap = cv.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

mouse = Controller()
detector = htm.handDetector(maxHands= 1)
pTime = 0
clicked = False

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    fingers, total = detector.findOpenFingers()

    if len(lmList)!= 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]
        cv.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 255, 255), 2)

        if fingers[1] == 1 and fingers[2] == 0:
            # print("Moving Mode")
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            cLocX = pLocX + (x3 - pLocX) / smoothening
            cLocY = pLocY + (y3 - pLocY) / smoothening

            mouse.position = (wScr - cLocX, cLocY)
            pLocX, pLocY = cLocX, cLocY
            cv.circle(img, (x1, y1), 10, (255, 255, 255), cv.FILLED)

        if fingers[1] == 1 and fingers[2] == 1:
            img, distance, points = detector.findDistance(img, 8, 12, draw= True)
            if distance < 20 and clicked == False:
                clicked = True
                cv.circle(img, (points[4], points[5]), 10, (0, 255, 0), cv.FILLED)
                mouse.click(Button.left)
            # print(distance, clicked)
            elif distance > 20:
                clicked = False
            if distance > 50:
                cv.circle(img, (points[4], points[5]), 10, (0, 0, 255), cv.FILLED)
                mouse.click(Button.right)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    cv.imshow("AIVirtualMouse", img)
    cv.waitKey(1)