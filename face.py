import cv2
from main.Steer import Steering
import RPi.GPIO as GPIO
import time

def init():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)
    GPIO.setup(38, GPIO.OUT)


def left_up():
	GPIO.output(12, True)
	GPIO.output(16, True)
	GPIO.output(18, True)
	GPIO.output(22, False)


def t_up():
	GPIO.output(12, True)
	GPIO.output(16, False)
	GPIO.output(18, True)
	GPIO.output(22, False)

def right_up():
	GPIO.output(12, True)
	GPIO.output(16, False)
	GPIO.output(18, True)
	GPIO.output(22, True)


def t_down():
	GPIO.output(12, False)
	GPIO.output(16, True)
	GPIO.output(18, False)
	GPIO.output(22, True)


def right_down():
	GPIO.output(12, False)
	GPIO.output(16, True)
	GPIO.output(18, True)
	GPIO.output(22, True)

def left_down():
	GPIO.output(12,  True)
	GPIO.output(16, True)
	GPIO.output(18,  False)
	GPIO.output(22, True)


def t_left():
	GPIO.output(12, False)
	GPIO.output(16, True)
	GPIO.output(18, True)
	GPIO.output(22, False)


def t_right():
	GPIO.output(12, True)
	GPIO.output(16, False)
	GPIO.output(18, False)
	GPIO.output(22, True)


def t_stop():
	GPIO.output(12, False)
	GPIO.output(16, False)
	GPIO.output(18, False)
	GPIO.output(22, False)

detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
steer=Steering(3,0,180,5,0,180,90,80) #初始位置为36和160，此时云台是正对前方，通过调试得到这两个值
steer.setup()
a=20
b=80
steer.specify(a,b)
f=0
while True and not f:
    ret, img = cap.read()
    shape=img.shape
    height= shape[0]
    width = shape[1]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        if not f:
            if w * h < 80 * 80:
                init()
                if y + h / 2 < height / 4:
                    t_down()
                else:
                    t_up()
                if x+w/2 < width/4:
                    t_right()
                elif x+w/2 > width/4*3:
                    t_left()
                time.sleep(0.1)
                t_stop()
            elif w * h > 200 * 200:
                init()
                t_down()
                time.sleep(0.1)
                t_stop()
            else:
                # 往左边
                if x+w/2 < width/2 and b < 180:
                    b += 3
                # 往右边
                elif b > 0:
                    b -= 3
                # 往前
                if y+h/2 < height/2 and a > 0:
                    a -= 3
                elif a < 90:
                    a += 3

            if abs(x+w/2 - width/2) < 90 and abs(y+h/2 - height/2) < 90 and w*h < 200*200 and w*h > 80*80:
                cv2.imwrite("1.jpg", img)
                f = 1
                break
            steer.specify(a, b)
    cv2.imshow('frame', img)
    cv2.waitKey(100)
    print(faces)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()