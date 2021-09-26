import cv2 as cv
import mediapipe as mp
import time
import math

class handDetector():
    def __init__(self, mode = False, maxHands = 2, minDetection = 0.5, minTracking = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.minDetection = minDetection
        self.minTracking = minTracking

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.minDetection, self.minTracking)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw = True):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLandmark in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLandmark, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw = False, drawBox = False):
        self.lmList = []
        xMin, yMin, xMax, yMax = 9999, 9999, 0, 0
        tolerance = 10
        bBox = []
        if self.results.multi_hand_landmarks:
            selectedHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(selectedHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                if cx < xMin:
                    xMin = cx
                if cx > xMax:
                    xMax = cx
                if cy < yMin:
                    yMin = cy
                if cy > yMax:
                    yMax = cy
                self.lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img, (cx, cy), 5, (255, 255, 255), cv.FILLED)
            if drawBox:
                cv.rectangle(img, (xMin - tolerance, yMin - tolerance), (xMax + tolerance, yMax + tolerance),
                             (255, 255, 255), 2)
            bBox = [xMin, yMin, xMax, yMax]
        return self.lmList, bBox

    def findOpenFingers(self):
        if len(self.lmList) != 0:
            fingers = []

            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)
            return fingers, totalFingers
        else:
            return [], 0

    def findOpenFingersVertical(self):
        if len(self.lmList) != 0:
            fingers = []

            if self.lmList[self.tipIds[0]][2] < self.lmList[self.tipIds[0] - 1][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][1] < self.lmList[self.tipIds[id] - 2][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)
            return fingers, totalFingers
        else:
            return [], 0

    def findDistance(self, img, id1, id2, draw = False):
        if len(self.lmList) != 0:
            x1, y1 = self.lmList[id1][1:]
            x2, y2 = self.lmList[id2][1:]
            mx, my = int((x1 + x2) / 2), int((y1 + y2) / 2)
            distance = math.hypot(x2 - x1, y2 - y1)
            points = []
            if draw:
                cv.line(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
                cv.circle(img, (x1, y1), 10, (255, 255, 255), cv.FILLED)
                cv.circle(img, (x2, y2), 10, (255, 255, 255), cv.FILLED)
                cv.circle(img, (mx, my), 10, (255, 255, 255), cv.FILLED)
            points = [x1, y1, x2, y2, mx, my]
            return img, distance, points

def main():
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList, bbox = detector.findPosition(img)

        if len(lmList) != 0:
            img, distance, points = detector.findDistance(img, 8, 12, draw= True)
            print(points)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

        cv.imshow("Hand Tracking", img)
        cv.waitKey(1)

if __name__ == "__main__":
    main()