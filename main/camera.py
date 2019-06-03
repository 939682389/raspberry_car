# camera.py
import cv2
from main.Steer import Steering
import time
from main.SQL import ImageHandler
class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        self.detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()
    def take_photo(self):
        ret, img = self.video.read()
        name = int(time.time())
        try:
            cv2.imwrite('/home/pi/car/main/static/images/%s.jpg' % name, img)
            image = ImageHandler.Image(image='%s.jpg' % name)
            ImageHandler.insert(image)
        except Exception as e:
            return e
        return '%s.jpg' % name
    def get_frame(self):
        # success, image = self.video.read()
        ret, img = self.video.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()