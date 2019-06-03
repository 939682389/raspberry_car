import RPi.GPIO as GPIO
import time

from gpiozero import Buzzer

Trig_Pin = 38
Echo_Pin = 40
Beep_pin = 13


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# 第3号针，GPIO2
GPIO.setup(Trig_Pin, GPIO.OUT, initial=GPIO.LOW)
# 第5号针，GPIO3
GPIO.setup(Echo_Pin, GPIO.IN)
# 第17号针，GPIO9
#GPIO.setup(Beep_pin, GPIO.OUT)
def checkdist():
    GPIO.output(Trig_Pin, GPIO.HIGH)
    time.sleep(0.00015)
    GPIO.output(Trig_Pin, GPIO.LOW)
    while not GPIO.input(Echo_Pin):
        pass
    t1 = time.time()
    while GPIO.input(Echo_Pin):
        pass
    t2 = time.time()
    return (t2-t1)*340/2

from gpiozero import TonalBuzzer
from gpiozero.tones import Tone
import time
b = TonalBuzzer(13)
def play(tone,freq, duration):
    b.play(tone) # 音调
    b.play(int(freq)) # 频率
    time.sleep(int(duration))
    b.stop()

#b.play(Tone(60))
#b.play("A4")
#b.play(220.0)
#b.play(60)
def buzz():
    play('A4', 500, 0.0005)


def beep():
    print('有人靠近！！！')
    GPIO.output(13, GPIO.LOW)
    time.sleep(0.5)
    GPIO.output(13, GPIO.HIGH)
    time.sleep(0.5)
    # GPIO.output(Beep_pin, GPIO.LOW)
    # time.sleep(0.5)
    # GPIO.output(Beep_pin, GPIO.HIGH)
    # time.sleep(0.5)


try:
    while True:
        print('距离: %0.2f m' % checkdist())
        if int(checkdist()) <= 1:
            buzz()
        time.sleep(0.5)
except KeyboardInterrupt:
    pass