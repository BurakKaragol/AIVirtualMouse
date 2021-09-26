import cv2 as cv
import mediapipe as mp
import time

class FaceDetector():
    def __init__(self, minDetectionCon = 0.5, modeSelection = 0):
        self.minDetectionCon = minDetectionCon
        self.modeSelection = modeSelection

        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon, self.modeSelection)

    def findFaces(self, img, draw = True, fancy = False):
        imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                       int(bboxC.width * iw), int(bboxC.height * ih)
                bboxs.append([id, bbox, detection.score])
                if fancy:
                    img = self.fancyDraw(img, bbox)
                if draw:
                    cv.rectangle(img, bbox, (255, 255, 255), 1)
                    cv.putText(img, f'{int(detection.score[0] * 100)}%', (bbox[0], bbox[1] - 10),
                               cv.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
        return img, bboxs

    def fancyDraw(self, img, bbox, l = 30, t = 5):
        x, y, w, h = bbox
        x1, y1 = x + w, y + h

        # #Top Left
        cv.line(img, (x, y), (x + l, y), (255, 255, 255), t)
        cv.line(img, (x, y), (x, y + l), (255, 255, 255), t)
        # Top right
        cv.line(img, (x1, y), (x1 - l, y), (255, 255, 255), t)
        cv.line(img, (x1, y), (x1, y + l), (255, 255, 255), t)
        # # Bottom Left
        cv.line(img, (x, y1), (x + l, y1), (255, 255, 255), t)
        cv.line(img, (x, y1), (x, y1 - l), (255, 255, 255), t)
        # # Bottom Right
        cv.line(img, (x1, y1), (x1 - l, y1), (255, 255, 255), t)
        cv.line(img, (x1, y1), (x1, y1 - l), (255, 255, 255), t)

        return img

def main():
    cap = cv.VideoCapture(0)
    pTime = 0
    detector = FaceDetector()

    while True:
        success, img = cap.read()
        img, bboxs = detector.findFaces(img)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)

        cv.imshow("Face Detection", img)
        cv.waitKey(1)

if __name__ == "__main__":
    main()