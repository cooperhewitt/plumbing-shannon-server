#!/usr/bin/env python

import cv2
import cv2.cv as cv
import numpy

class finder:
        
        def __init__(self):

                self.img = None

        def load_from_path(self, path):

		img = cv2.imread(path, cv2.CV_LOAD_IMAGE_COLOR)
                self.img = img

        def load_from_camera(self, camera=0):

                vidcap = cv2.VideoCapture()
                vidcap.open(camera)

                retval, img = vidcap.retrieve()
                vidcap.release()

                self.img = img

        def detect_faces(self, rules="haarcascade_frontalface_alt.xml"):
                return self.detect(rules)

        def detect_eyes(self, rules="haarcascade_eye.xml"):
                return self.detect(rules)

                """
                storage = cv.CreateMemStorage()
                rects = cv.HaarDetectObjects(self.img, rules, storage)
                return rects
                """

        def detect(self, rules):

                cascade = cv2.CascadeClassifier(rules)
                rects = cascade.detectMultiScale(self.img, scaleFactor=1.1, minNeighbors=3, minSize=(10, 10), flags = cv.CV_HAAR_SCALE_IMAGE)

                if len(rects) == 0:
                        return None

                rects[:,2:] += rects[:,:2]
                return rects

        def draw_rectangles(self, rects, color=(0, 255, 0)):

                for x1, y1, x2, y2 in rects:
                        cv2.rectangle(self.img, (x1, y1), (x2, y2), color, 2)
                        
        def save(self, path):
                cv2.imwrite(path, self.img)

        def show(self):

                cv2.namedWindow('Display image')
                cv2.imshow('Display image', self.img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

if __name__ == '__main__':

        import sys
        # path = sys.argv[1]

        f = finder()

        f.load_from_camera()

        faces = f.detect_faces()
        eyes = f.detect_eyes()

        print faces
        print eyes

        r = numpy.concatenate((faces, eyes))

        f.draw_rectangles(r)

        f.show()

        # f.save('test2.jpg')
        
        sys.exit()
