import cv2 as cv
import numpy as np
import time
import os
import HandTrackingModule as htm

cap = cv.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
pTime = 0
detector = htm.handDetector(maxHands=1, minDetection=0.75)

folderPath = "borders"
myList = os.listdir(folderPath)
overlayList = []

for imPath in myList:
    image = cv.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

header = overlayList[0]
drawColor = (0, 0, 255)
brushThickness = 15
eraserThickness = 45
xp, yp = 0, 0
imgCanvas = np.zeros([720, 1280, 3], np.uint8)

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)

    img = detector.findHands(img)
    lmlist, _ = detector.findPosition(img)
    if len(lmlist) != 0:
        x1, y1 = lmlist[8][1:] #isaret parmagi
        x2, y2 = lmlist[12][1:] #orta parmak

        fingers, total = detector.findOpenFingers()
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0
            # print("Selection Mode")
            if y1 < 145:
                if 350 < x1 < 500:
                    drawColor = (0, 0, 255)
                    header = overlayList[0]
                elif 550 < x1 < 750:
                    drawColor = (0, 255, 0)
                    header = overlayList[1]
                elif 800 < x1 < 950:
                    drawColor = (255, 0, 0)
                    header = overlayList[2]
                elif 1000 < x1 < 1200:
                    drawColor = (0, 0, 0)
                    header = overlayList[3]
            cv.rectangle(img, (x1- 10, y1 - 25), (x2 + 10, y2 + 25), drawColor, cv.FILLED)

        if fingers[1] and fingers[2] == False:
            # print("Drawing Mode")
            # cv.circle(img, (x1, y1), 15, drawColor, cv.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            # cv.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)

            if drawColor == (0, 0, 0):
                cv.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv.circle(img, (x1, y1), int(eraserThickness / 2), drawColor, cv.FILLED)
            else:
                cv.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv.circle(img, (x1, y1), int(brushThickness / 2), drawColor, cv.FILLED)

            xp, yp = x1, y1

    imgGray = cv.cvtColor(imgCanvas, cv.COLOR_BGR2GRAY)
    _, imgInv = cv.threshold(imgGray, 10, 255, cv.THRESH_BINARY_INV)
    imgInv = cv.cvtColor(imgInv, cv.COLOR_GRAY2BGR)
    img = cv.bitwise_and(img, imgInv)
    img = cv.bitwise_or(img, imgCanvas)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    img[0:151, 0:1280] = header
    # img = cv.addWeighted(img, 0.5, imgCanvas, 0.5, 0)

    cv.putText(img, str(int(fps)), (10, 200), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    cv.imshow("Virtual Painter", img)
    cv.waitKey(1)