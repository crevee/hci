import sys, os, time
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QObject, QTimer, Slot, Signal
from PySide6.QtGui import *

class AnimationViewer(QLabel):
    def __init__(self, _parent = None):
        super(AnimationViewer, self).__init__(_parent)
        self.image = QImage()

        self.timer = QTimer()
       # self.timer.timeout.connect(self._play) # connect it function
        

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

    def initUI(self):
        self.setWindowTitle('Test')

    @Slot(QImage)
    def setImage(self, image):
        if image.isNull():
            print("Viewer Dropped frame!")

        self.image = image
        if image.size() != self.size():
            self.setFixedSize(image.size())
        self.repaint()

class PlaylistManager(QObject):
    def __init__(self, _parent = None):
        super(PlaylistManager, self).__init__(_parent)
        self.obj = _parent
        print(f"In PlaylistManager {self.obj}")

    def add_animation(self):
        # retrieve txtEdit content
		# add the contents to the playList
		# exceptional case: check null string

        if(self.obj.textEdit.toPlainText() != ""):
            self.obj.playlist.addItem(self.obj.textEdit.toPlainText())
        self.obj.textEdit.setPlainText("")

    def remove_animation(self):
        if(self.obj.playlist.currentRow() > -1):
            self.obj.playlist.takeItem(self.obj.playlist.currentRow())
            
    def up_animation(self):
		# if currentRow <= 0 skip
		# currentRow > 0 then process
        if(self.obj.playlist.currentRow() > 0):
            prev_item = self.obj.playlist.item(self.obj.playlist.currentRow() - 1)
            self.obj.playlist.takeItem(self.obj.playlist.currentRow() - 1)
            self.obj.playlist.insertItem(self.obj.playlist.currentRow() + 1, prev_item.text())


    def down_animation(self):
		# self.playList.count()
        if(self.obj.playlist.currentRow() < self.obj.playlist.count() - 1):
            next_item = self.obj.playlist.item(self.obj.playlist.currentRow() + 1)
            self.obj.playlist.takeItem(self.obj.playlist.currentRow() + 1)
            self.playlist.insertItem(self.obj.playlist.currentRow(), next_item.text())

    def __getattr__(self, attr):
        return getattr(self.obj, attr)

class MediaControl(QObject):
    # signal part
    VIDEO_SIG = Signal(QImage)

    def __init__(self, _parent = None):
        super(MediaControl, self).__init__(_parent)
        self.obj = _parent

        self.timer = QTimer()
        self.timer.timeout.connect(self.send_image)

        self.current_animation = 0
        self.current_row_idx = 0
        self.curent_image_idx = 0


    def get_animation(self, _path):
        path = _path
        file_list = os.listdir(path)

        images_lst = []
        for file in file_list:
            image = QImage()
            image.load(path + file)
            images_lst.append(image)

        return images_lst

    @Slot()
    def send_image(self):

        #self.obj.playlist.count() - 1):
        # if(self.obj.playlist.currentRow() < self.obj.playlist.count() - 1):
        #for list in range(self.get_animation(self.obj.playlist.currentItem().text()), self.get_animation(self.obj.playlist.item(self.obj.playlist.count() - 1).text())):

        self.timer.setInterval(1000)
        self.timer.start()

        for frame in self.get_animation(self.obj.playlist.currentItem().text()):
            if(self.timer.isActive() == True):
                self.timer.timeout.connect(self.obj.label.setImage(frame))
                app.processEvents()
                time.sleep(0.1)
            


    def play_animation(self):

        #if(self.current_animation > self.obj.playlist.count):
        #    self.current_animation  = 0

        #current_animation += 1    
        #self.obj.playlist.item(self.obj).playlist.currentRow().text
        print(self.obj.playlist.currentItem().text())
        #self.get_animation(self.obj.playlist.currentItem().text())
        # When play button is clicked
        # get animaion -> from where? to send? send what?
        self.send_image()


    def pause_animation(self):
        self.timer.stop()
        print("pause")

    def resume_animation(self):
        self.timer.start()
        print("resume")

    def stop_animation(self):
        
        control_key = False

        for frame in self.get_animation(self.obj.playlist.item(0).text()):
            if(self.timer.isActive() == True):
                self.timer.timeout.connect(self.obj.label.setImage(frame))
                app.processEvents()
                time.sleep(0.1)
        print("stop")

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
        self.obj.addbtn.clicked.connect(self.playlist_manager.add_animation)
        self.obj.removebtn.clicked.connect(self.playlist_manager.remove_animation)
        self.obj.upbtn.clicked.connect(self.playlist_manager.up_animation)
        self.obj.downbtn.clicked.connect(self.playlist_manager.down_animation)

        self.obj.startbtn.clicked.connect(self.media_control.play_animation)
        self.obj.pausebtn.clicked.connect(self.media_control.pause_animation)
        self.obj.resumebtn.clicked.connect(self.media_control.resume_animation)
        self.obj.stopbtn.clicked.connect(self.media_control.stop_animation)



        self.media_control.VIDEO_SIG.connect(self.obj.label.setImage)

    def __getattr__(self, attr):
        return getattr(self.obj, attr)

    
    def show(self):
        self.obj.show()

# Create a Qt application
app = QApplication(sys.argv)

ui_file = QFile("/Users/HaSangWook/HCI/2st_project/stop_motion_player.ui")
loader = QUiLoader()
window = loader.load(ui_file)
ui_file.close()

smp = StopMotionPlayer(window)
smp.show()
# Enter Qt application main loop
sys.exit(app.exec())