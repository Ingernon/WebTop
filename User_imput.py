from threading import Thread
import time
import win32api
import win32con

class User_imput(Thread):
	def __init__(self):

		super(User_imput, self).__init__()
		self.stop = False
		self.keys = []
		self.mouse = []
		self.click = []
		self.act_keys = []

	def get_keys_state(self):
		self.act_keys = []
		for i in range(255):
			if win32api.GetAsyncKeyState(i):
				self.act_keys.append(i)

	def release_key(self):
		dif = []
		for n in self.act_keys:
			if n not in self.keys:
				dif.append(n)
		for i in dif:
			win32api.keybd_event(i,0,win32con.KEYEVENTF_KEYUP,0)

	def press_key(self):
		dif = []
		for n in self.keys:
			if n not in self.act_keys:
				dif.append(n)
		for i in dif:
			win32api.keybd_event(i,0,0)

	def move_mouse(self):
		win32api.SetCursorPos((self.mouse[0],self.mouse[1]))

	def click_down(self):
		win32api.SetCursorPos((self.mouse[0],self.mouse[1]))
		if 1 in self.click:
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,self.mouse[0],self.mouse[1],0,0)
		if 2 in self.click:
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,self.mouse[0],self.mouse[1],0,0)
			win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,self.mouse[0],self.mouse[1],0,0)

	def click_up(self):
		win32api.SetCursorPos((self.mouse[0],self.mouse[1]))
		if 1 not in self.click:
			win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,self.mouse[0],self.mouse[1],0,0)
		#if 2 not in self.click:
			#win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,self.mouse[0],self.mouse[1],0,0)

	def run(self):
		# while not self.stop:
		self.get_keys_state()
		print(self.keys, self.act_keys)
		self.move_mouse()
		self.click_down()
		self.click_up()
		self.press_key()
		self.release_key()

if __name__ == '__main__':
	for i in range(255):
		win32api.keybd_event(i,0,win32con.KEYEVENTF_KEYUP,0)