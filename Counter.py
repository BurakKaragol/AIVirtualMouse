import cv2 as cv
import mediapipe as mp
import numpy as np
import time

class handDetector():
    def __init__(self, mode = False, maxHands = 2, minDetection = 0.5, minTracking = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.minDetection = minDetection
        self.minTracking = minTracking

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.minDetection, self.minTracking)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLandmark in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmark, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw = False):
        lmList = []
        fingers = []
        distances = []
        if self.results.multi_hand_landmarks:
            selectedHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(selectedHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 5, (255, 255, 255), cv.FILLED)
                #Her parmagin uzunlugunu parmak uzunlugu olarak degil
                #bilekten aciklik oalarak hesaplarsak daha tutarli olur
                if id == 2 or id == 3 or id == 4: #Bas parmak
                    if id == 2:
                        fingers.clear()
                    fingers.append([id, cx, cy])
                    if id == 4:
                        dist = self.fingerChecker(fingers, 3)
                        distances.append(dist)
                if id == 5 or id == 6 or id == 7 or id == 8: #Isaret parmagi
                    if id == 5:
                        fingers.clear()
                    fingers.append([id, cx, cy])
                    if id == 8:
                        dist = self.fingerChecker(fingers, 4)
                        distances.append(dist)
                if id == 9 or id == 10 or id == 11 or id == 12: #Orta parmak
                    if id == 9:
                        fingers.clear()
                    fingers.append([id, cx, cy])
                    if id == 12:
                        dist = self.fingerChecker(fingers, 4)
                        distances.append(dist)
                if id == 13 or id == 14 or id == 15 or id == 16: #Yuzuk parmagi
                    if id == 13:
                        fingers.clear()
                    fingers.append([id, cx, cy])
                    if id == 16:
                        dist = self.fingerChecker(fingers, 4)
                        distances.append(dist)
                if id == 17 or id == 18 or id == 19 or id == 20: #Serce parmagi
                    if id == 17:
                        fingers.clear()
                    fingers.append([id, cx, cy])
                    if id == 20:
                        dist = self.fingerChecker(fingers, 4)
                        distances.append(dist)
                # print(distances)
        return lmList, distances

    def fingerChecker(self, finger, pointNum):
        xPoints = []
        yPoints = []
        for point in finger:
            xPoints.append(point[1])
            yPoints.append(point[2])
        distance = self.distCalc(xPoints, yPoints)
        return distance

    def distCalc(self, xPoints, yPoints):
        p1x, p1y = xPoints[0], yPoints[0]
        p2x, p2y = xPoints[-1], yPoints[-1]
        # print(xPoints, yPoints)
        # print(p1x, p1y, p2x, p2y)
        d1 = abs(p1x - p2x)
        d2 = abs(p1y - p2y)
        dist = np.sqrt(pow(d1, 2) + pow(d2, 2))
        # print(dist)
        return dist

    def counter(self, distances):
        count = 0
        if len(distances) == 5:
            if distances[0] >= 60:
                count += 1
            if distances[1] >= 100:
                count += 1
            if distances[2] >= 120:
                count += 1
            if distances[3] >= 90:
                count += 1
            if distances[4] >= 80:
                count += 1
        return count

def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, distances = detector.findPosition(img)
        count = detector.counter(distances)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
        cv.putText(img, str(count), (10, 100), cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

        cv.imshow("Finger Counter", img)
        cv.waitKey(1)

if __name__ == "__main__":
    main()