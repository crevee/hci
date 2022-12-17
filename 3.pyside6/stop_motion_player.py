# Todo
## 1. Design your program using Qt Designer
## 2. Complete the Stop Motion Player software

import sys
import os

from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QObject, QTimer, Slot, Signal
from PySide6.QtGui import *

class AnimationViewer(QLabel):
	def __init__(self, _parent=None):
		super(AnimationViewer, self).__init__(_parent)
		self.image = QImage()
		pass

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.drawImage(0, 0, self.image)

	def initUI(self):
		self.setWindowTitle('Test')

	@Slot(QImage)
	def setImage(self, image):
		pass

class PlaylistManager(QObject):
	def __init__(self, _parent=None):
		super(PlaylistManager, self).__init__(_parent)
		self.obj = _parent
		print(f"In PlaylistManager {self.obj}")
		pass

	def add_animation(self):
		# retrieve txtEdit content
		# add the contents to the playList
		# exceptional case: check null string
		pass

	def remove_animation(self):
		pass

	def up_animation(self):
		# if currentRow <= 0 skip
		# currentRow > 0 then process
		pass

	def down_animation(self):
		# self.playList.count()
		pass

	def __getattr__(self, attr):
		return getattr(self.obj, attr)

class MediaControl(QObject):
	# signal part
	VIDEO_SIG = Signal(QImage)

	def __init__(self, _parent = None):
		super(MediaControl, self).__init__(_parent)
		self.obj = _parent

		pass

	def get_animation(self, _path):
		pass

	@Slot()
	def send_image(self):
		#print("send")

		
		pass

	def play_animation(self):
		print("play")

		# When play button is clicked 
		# get animation -> from where?, send to? send what?
		pass

	def pause_animation(self):
		
		pass

	def resume_animation(self):
		
		pass

	def stop_animation(self):
		
		pass	

	def __getattr__(self, attr):
		return getattr(self.obj, attr)

class StopMotionPlayer(QWidget):
	def __init__(self, _parent = None):
		super(StopMotionPlayer, self).__init__(_parent)
		self.obj = _parent

		self.media_control = MediaControl(self.obj)
		self.playlist_manager = PlaylistManager(self.obj)

		self.obj.label = AnimationViewer(self.obj.label)
		
		# Event handling
		pass
		

	def __getattr__(self, attr):
		return getattr(self.obj, attr)

	def show(self):
		self.obj.show()

# Create a Qt application
app = QApplication(sys.argv)

ui_file = QFile("project02.ui")
loader = QUiLoader()
window = loader.load(ui_file)
ui_file.close()

print("components of main window")
print(window.__dict__.keys())

smp = StopMotionPlayer(window)
smp.show()
# Enter Qt application main loop
sys.exit(app.exec())