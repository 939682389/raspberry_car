
from flask import Flask, request, session, g, redirect, url_for, \
abort, render_template, flash, make_response
from contextlib import closing
from flask_sqlalchemy import SQLAlchemy
import main.SQL.mysql_config as config
from datetime import timedelta
import os

app = Flask(__name__)

app.config.from_object(config)
db = SQLAlchemy(app)
app.config['SEND_FILE_MAX_AGE_DEFAULT']=timedelta(seconds=1)
app.config['SECRET_KEY']=os.urandom(24)   #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=7) #设置session的保存时间。
basedir = os.path.abspath(os.path.dirname(__file__))

from main.Temps import Temps
from main.SQL import TempHandler
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash,jsonify, Response
from contextlib import closing
from flask import Flask, render_template, Response

# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
from main.camera import VideoCamera
import re
import RPi.GPIO as GPIO
import time
import signal
import atexit
from main.Steer import Steering
import time
 #初始位置为36和160，此时云台是正对前方，通过调试得到这两个值


@app.route('/home')
def show_index():
	return render_template('home.html')


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method=="GET":
		return "get"+request.form["user"]
	elif request.method=="POST":
		return "post"


@app.route('/ctl',methods=['GET','POST'])
def ctrl_id():
	if request.method == 'POST':
		id = request.form['id']
		GPIO.setmode(GPIO.BOARD)
		GPIO.setwarnings(False)
		GPIO.setup(11,GPIO.OUT)
		GPIO.setup(12,GPIO.OUT)
		GPIO.setup(15,GPIO.OUT)
		GPIO.setup(16,GPIO.OUT)
		GPIO.setup(18, GPIO.OUT)
		GPIO.setup(22, GPIO.OUT)
		GPIO.setup(38,GPIO.OUT)


		if id == 't_left':
			t_left()
			time.sleep(0.5)
			t_stop()
			return jsonify({"msg":"left"})
		elif id == 't_right':
			t_right()
			time.sleep(0.5)
			t_stop()
			return jsonify({"msg":"right"})
		elif id == 't_up':
			t_up()
			time.sleep(0.5)
			t_stop()
			return jsonify({"msg":"up"})
		elif id == 't_down':
			t_down()
			time.sleep(0.5)
			t_stop()
			return jsonify({"msg" : "down"})
		elif id == 't_stop':
			t_stop()
			return jsonify({"msg" : "stop"})
		elif id == 't_servo':
			t_stop()
			return "servo"
		elif id=="l_left":
			t_left()
			return jsonify({"msg": "left"})
		elif id == 'l_right':
			t_right()
			return jsonify({"msg":"right"})
		elif id == 'l_up':
			t_up()
			return jsonify({"msg":"up"})
		elif id == 'l_down':
			t_down()
			return jsonify({"msg":"down"})
		elif id=="ladd" or id=='lred':
			lroa = request.form['lroa']
			hroa = request.form['hroa']
			steer = Steering(3, 0, 180, 5, 90, 180, 90, 80)
			steer.setup()
			steer.specify(int(hroa), int(lroa))
			print(lroa)
			return jsonify({"msg": "ladd"})
	return redirect(url_for('show_index'))


def t_stop():
	GPIO.output(12, False)
	GPIO.output(16, False)
	GPIO.output(18, False)
	GPIO.output(22, False)


def t_up():
	GPIO.output(12, True)
	GPIO.output(16, False)
	GPIO.output(18, True)
	GPIO.output(22, False)


def t_down():
	GPIO.output(12, False)
	GPIO.output(16, True)
	GPIO.output(18, False)
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

def t_servo():
	atexit.register(GPIO.cleanup)
	servopin = 38
	GPIO.setup(servopin, GPIO.OUT, initial=False)
	p = GPIO.PWM(servopin,50)
	p.start(0)
	time.sleep(2)
	for i in range(0,181,10):
		p.ChangeDutyCycle(2.5 + 10 * i / 180)
		time.sleep(0.02)
		p.ChangeDutyCycle(0)
		time.sleep(0.2)
	for i in range(181,0,-10):
		p.ChangeDutyCycle(2.5 + 10 * i / 180)
		time.sleep(0.02)
		p.ChangeDutyCycle(0)
		time.sleep(0.2)



@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/takePhoto')
def takePhoto():
	res={}
	camera = VideoCamera()
	res['data'] = camera.take_photo()
	return jsonify(res)

@app.route('/img/<string:filename>', methods=['GET'])
def show_photo(filename):
    if request.method == 'GET':
        if filename is None:
            pass
        else:
            image_data = open((os.path.join(basedir, 'static', 'images/%s' % filename)), "rb").read()
            response = make_response(image_data)
            response.headers['Content-Type'] = 'image/png'
            return response
    else:
        pass
@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/temp')
def now_temp():
	temp = Temps()
	res = temp.getDHT()
	return jsonify(res)

@app.route('/temp/get')
def get_temp():
    res={}
    res['data'] = TempHandler.query_end().to_json()
    return jsonify(res['data'])


