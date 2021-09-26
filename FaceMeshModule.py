import cv2 as cv
import mediapipe as mp
import time

class FaceMeshDetector():
    def __init__(self, mode = False, maxFace = 1, minDetectionCon = 0.5, minTrackingCon = 0.5):
        self.mode = mode
        self.maxFace = maxFace
        self.minDetectionCon = minDetectionCon
        self.minTrackingCon = minTrackingCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(self.mode, self.maxFace, self.minDetectionCon, self.minTrackingCon)
        self.drawSpecs = self.mpDraw.DrawingSpec(thickness = 1, circle_radius = 2)

    def findFaceMesh(self, img, draw = True):
        self.imgRGB = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        faces = []

        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, faceLms, self.mpFaceMesh.FACEMESH_CONTOURS,
                                           self.drawSpecs, self.drawSpecs)
                face = []
                for id, lm in enumerate(faceLms.landmark):
                    # print(id, lm)
                    ih, iw, ic = img.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)
                    face.append([id, x, y])
                    # print(id, x, y)
                faces.append(face)
        return img, faces

def main():
    cap = cv.VideoCapture(0)
    pTime = 0
    detector = FaceMeshDetector()

    while True:
        success, img = cap.read()
        img, faces = detector.findFaceMesh(img)

        if len(faces) != 0:
            print(faces)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv.putText(img, str(int(fps)), (10, 50), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
        cv.imshow("Face Mesh", img)
        cv.waitKey(1)


if __name__ == "__main__":
    main()