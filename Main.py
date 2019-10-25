import flask as fl
from ast import literal_eval
import time
import numpy as np

from Capture import VideoFeed
import User_imput

def loop(feed):
	while True:
		start_time = time.time()
		frame = feed.get_frame()
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
		time.sleep(max(1./30 - (time.time() - start_time), 0))

app = fl.Flask(__name__)
app.secret_key = "ineedtohaveabetterkey" #this is true

@app.route('/')
def index():
	fl.session['id']= str(np.random.randint(-999999999, 999999999)) #also need to change this
	return fl.render_template('webtop.html')

@app.route('/postkeys', methods=['GET', 'POST'])
def postkeys():
	if 'id' in fl.session:
		s = fl.session['id'];
	rep = literal_eval(str(fl.request.data).split("\'")[1])
	ui = User_imput.User_imput()
	ui.keys = rep["keys"]
	ui.mouse = rep["mouse"]
	ui.click = rep["click"]
	ui.start()
	return ""

@app.route('/video_feed')
def video_feed():
	if 'id' in fl.session:
		s = fl.session['id'];
	return fl.Response(loop(VideoFeed()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
	app.run(host='localhost', debug=True)
	#app.run(host='192.168.137.1', debug=True)