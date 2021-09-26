import cv2 as cv
import numpy as np
import time
import HandTrackingModule as htm
import random

pTime = 0
countDown = 5
startCount = False
handTypes = ["Rock", "Paper", "Scissors"]
pcHandSelected = False
humanScore = 0
pcScore = 0
scoreSaved = False

camW, camH = 640, 480
cap = cv.VideoCapture(0)
cap.set(3, camW)
cap.set(4, camH)

detector = htm.handDetector(maxHands= 1)

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw= False)
    lmList, bbox = detector.findPosition(img, drawBox= True)
    fingers, totalFingers = detector.findOpenFingersVertical()

    if len(lmList) != 0:
        if startCount == False:
            startCount = True
            startTime = time.time()
            timeLeft = countDown
            displayTime = countDown

        if scoreSaved == False:
            if fingers == [0, 0, 0, 0, 0]:
                humanHand = handTypes[0]
            elif fingers == [1, 1, 1, 1, 1]:
                humanHand = handTypes[1]
            elif fingers == [0, 1, 1, 0, 0]:
                humanHand = handTypes[2]

        if timeLeft >= 0:
            timeLeft = countDown - (time.time() - startTime)
            displayTime = format(timeLeft, ".2f")
            cv.putText(img, displayTime, (100, 100), cv.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
        else:
            cv.putText(img, "0.00", (100, 100), cv.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
            if pcHandSelected == False:
                rand = random.randrange(0, 3, 1)
                pcHand = handTypes[rand]
                pcHandSelected = True
            cv.putText(img, pcHand, (300, 100), cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)

            if humanHand == "Rock":
                if pcHand == "Rock":
                    cv.putText(img, "draw", (300, 150), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
                    if scoreSaved == False:
                        scoreSaved = True
                if pcHand == "Paper":
                    cv.putText(img, "lose", (300, 150), cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                    if scoreSaved == False:
                        pcScore += 1
                        scoreSaved = True
                if pcHand == "Scissors":
                    cv.putText(img, "win", (300, 150), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    if scoreSaved == False:
                        humanScore += 1
                        scoreSaved = True
            if humanHand == "Paper":
                if pcHand == "Rock":
                    cv.putText(img, "win", (300, 150), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    if scoreSaved == False:
                        humanScore += 1
                        scoreSaved = True
                if pcHand == "Paper":
                    cv.putText(img, "draw", (300, 150), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
                    if scoreSaved == False:
                        scoreSaved = True
                if pcHand == "Scissors":
                    cv.putText(img, "lose", (300, 150), cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                    if scoreSaved == False:
                        pcScore += 1
                        scoreSaved = True
            if humanHand == "Scissors":
                if pcHand == "Rock":
                    cv.putText(img, "lose", (300, 150), cv.FONT_HERSHEY_PLAIN, 3, (0, 0, 255), 3)
                    if scoreSaved == False:
                        pcScore += 1
                        scoreSaved = True
                if pcHand == "Paper":
                    cv.putText(img, "win", (300, 150), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
                    if scoreSaved == False:
                        humanScore += 1
                        scoreSaved = True
                if pcHand == "Scissors":
                    cv.putText(img, "draw", (300, 150), cv.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)
                    if scoreSaved == False:
                        scoreSaved = True

        cv.putText(img, f'{humanScore} - {pcScore}', (10, 450), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    else:
        startCount = False
        pcHandSelected = False
        scoreSaved = False

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime


    cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    cv.imshow("Rock Paper Scissors", img)
    cv.waitKey(1)