from flask import Flask, render_template, Response, request
from Capture import VideoFeed
import time
import User_imput
from ast import literal_eval


def loop(camera):
	while True:
		start_time = time.time()
		frame = camera.get_frame()
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		time.sleep(max(1./30 - (time.time() - start_time), 0))

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/getkeys')
def getkeys():
	return render_template('app/getkeys.js')

@app.route('/postkeys', methods=['GET', 'POST'])
def postkeys():
	rep = literal_eval(str(request.data).split("\'")[1])
	ui = User_imput.User_imput()
	ui.keys = rep["keys"]
	ui.mouse = rep["mouse"]
	ui.click = rep["click"]
	ui.start()
	return ""

@app.route('/video_feed')
def video_feed():
	return Response(loop(VideoFeed()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	#app.run(host='localhost', debug=True)
	app.run(host='192.168.137.1', debug=True)