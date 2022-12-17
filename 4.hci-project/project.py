import sys

from PySide6.QtWidgets import *
from PySide6.QtCore import QRect, QCoreApplication, Slot, Signal
from PySide6.QtGui import QImage, QPainter

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from io import BytesIO

class ImageViewer(QLabel):
	def __init__(self, _parent=None):
		super(ImageViewer, self).__init__(_parent)
		self.image = QImage()
		pass

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.drawImage(0, 0, self.image)

	def initUI(self):
		self.setWindowTitle('Test')

	@Slot(QImage)
	def setImage(self, image:QImage):
		if image.isNull():
			print("Viewer Dropped frame!")

		self.image = image
		if image.size() != self.size():
			self.image = self.image.scaled(self.size())
		self.repaint()  

class TelegramBotUI(QMainWindow):
    VIDEO_SIG = Signal(QImage)
    def __init__(self, _parent = None):
        super(TelegramBotUI, self).__init__(_parent)
        self.resize(485*2, 604)
        self.centralwidget = QWidget(self)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QRect(10, 10, 461, 91))

        self.img_groupBox = QGroupBox(self.centralwidget)
        self.img_groupBox.setGeometry(QRect(471, 10, 461, 571))

        self.image = ImageViewer(self)
        self.image.setGeometry(QRect(475, 30, 485*2-20, 561))

        self.telegramEdit = QTextEdit(self.groupBox)
        self.telegramEdit.setGeometry(QRect(10, 30, 331, 31))
        self.telegramBtn = QPushButton(self.groupBox)
        self.telegramBtn.setGeometry(QRect(350, 30, 75, 31))
        self.Chat = QGroupBox(self.centralwidget)
        self.Chat.setGeometry(QRect(10, 110, 461, 391))
        self.listView = QListWidget(self.Chat)
        self.listView.setGeometry(QRect(10, 20, 441, 361))
        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QRect(10, 500, 461, 61))
        self.sendBtn = QPushButton(self.groupBox_3)
        self.sendBtn.setGeometry(QRect(360, 20, 91, 31))
        self.contentEdit = QTextEdit(self.groupBox_3)
        self.contentEdit.setGeometry(QRect(10, 20, 331, 31))
        
        self.setCentralWidget(self.centralwidget)

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QRect(0, 0, 485, 22))
        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)
        
        self.retranslateUi()

        self.telegramBtn.clicked.connect(self.qt_handle_telegram)
        self.sendBtn.clicked.connect(self.qt_handle_send)
        
        self.VIDEO_SIG.connect(self.image.setImage)

        self.updater = Updater("Your Telegram Token")

        # Get the dispatcher to register handlers
        dispatcher = self.updater.dispatcher

        # on non command i.e message - echo the message on Telegram
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.tg_echo))
        dispatcher.add_handler(MessageHandler(Filters.photo, self.tg_handle_image))
        self.updater.start_polling()

        self.telegram_id = None

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("MainWindow", u"Telegram Chat Bot UI", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Telegram ID", None))
        self.telegramBtn.setText(QCoreApplication.translate("MainWindow", u"Confirm", None))
        self.Chat.setTitle(QCoreApplication.translate("MainWindow", u"Chat Log", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Contents", None))
        self.img_groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Image", None))
        self.image.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.sendBtn.setText(QCoreApplication.translate("MainWindow", u"Send", None))

    #### task 01
    def tg_echo(self, update: Update, context: CallbackContext) -> None:
        pass

    #### task 02
    def qt_handle_telegram(self): 
        pass

    #### task 03
    def qt_handle_send(self):
        pass
    
    #### task 04
    def tg_handle_image(self, update: Update, context: CallbackContext):
        pass

    def closeEvent(self, event):
        self.updater.stop()
        self.updater.is_idle = False
        event.accept()

# Create a Qt application
app = QApplication(sys.argv)

tbu = TelegramBotUI()
tbu.show()

# Enter Qt application main loop
sys.exit(app.exec())
