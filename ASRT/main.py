import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, \
	QAction, qApp, QTextEdit, QWidget, QFileDialog, QLabel, QVBoxLayout, QGridLayout

from PyQt5.QtGui import QIcon, QPixmap, QPalette, QFont
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.Qt import QLineEdit
from PyQt5.QtMultimedia import  QSound
import playsound
import VoiceAnalasis
import VoiceRecord
import time

from scipy.io.wavfile import write

from SpeechModel251 import ModelSpeech
from LanguageModel2 import ModelLanguage
from keras import backend as K

class Example(QMainWindow):

	def __init__(self):
		super().__init__()
		self.central_widget = QWidget()
		self.file_label = QLabel('File Name')
		self.file_path_label = QLabel('File Path')
		self.file_path = ''
		self.predict = QLabel('Result')
		self.png = QLabel('Picture')
		self.initUI()


	def initUI(self):
		# 退出函数
		exitAction = QAction('&Exit', self)
		exitAction.setShortcut('Ctrl+1')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)

		# 打开文件
		openfile = QAction('Open', self)
		openfile.setShortcut('Ctrl+2')
		openfile.setStatusTip('Open new file')
		openfile.triggered.connect(self.choose_file)

		# 播放原语音
		playsound = QAction('Play sound', self)
		playsound.setShortcut('Ctrl+8')
		playsound.setStatusTip('Play original Sound')
		playsound.triggered.connect(self.play_sound)

		# 录制声音
		recordsound = QAction('Record sound', self)
		recordsound.setShortcut('Alt+1')
		recordsound.setStatusTip('Record a wav sound file')
		recordsound.triggered.connect(self.record_sound)

		# 识别语音
		recognizefile = QAction('Recognize', self)
		recognizefile.setShortcut('Ctrl+3')
		recognizefile.setStatusTip('Recognize the File you just open')
		recognizefile.triggered.connect(self.plot_recognize_result)

		# 生成wave.png
		get_wave = QAction('Get wave', self)
		get_wave.setShortcut('Ctrl+4')
		get_wave.setStatusTip('Generate WAVE plot for the chosen voice')
		get_wave.triggered.connect(self.plot_wave)

		# spec.png
		get_spec = QAction('Get spec', self)
		get_spec.setShortcut('Ctrl+5')
		get_spec.setStatusTip('Generate SPEC plot for the chosen voice')
		get_spec.triggered.connect(self.plot_spec)

		# CQT.png
		get_CQT = QAction('Get CQT', self)
		get_CQT.setShortcut('Ctrl+6')
		get_CQT.setStatusTip('Generate CQT plot for the chosen voice')
		get_CQT.triggered.connect(self.plot_CQT)

		# mfcc.png
		get_mfcc = QAction('Get MFCC', self)
		get_mfcc.setShortcut('Ctrl+7')
		get_mfcc.setStatusTip('Generate MFCC plot for the chosen voice')
		get_mfcc.triggered.connect(self.plot_mfcc)

		# 文本框

		# 布局

		grid = QGridLayout()
		grid.setSpacing(50)
		# QWidget* widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = 0
		grid.addWidget(self.file_label, 0, 0)
		grid.addWidget(self.file_path_label, 0, 1)
		grid.addWidget(self.predict, 1, 0, 1, 2)
		grid.addWidget(self.png, 2, 0, 1, 2)
		# menubar
		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(openfile)
		fileMenu.addAction(exitAction)
		fileMenu.addAction(playsound)
		fileMenu.addAction(recordsound)

		recognizeMenu = menubar.addMenu('&Recognize')
		recognizeMenu.addAction(recognizefile)

		picMenu = menubar.addMenu('&Analysis')
		picMenu.addAction(get_wave)
		picMenu.addAction(get_spec)
		picMenu.addAction(get_CQT)
		picMenu.addAction(get_mfcc)

		# toolbar = self.addToolBar('&Exit')
		# toolbar.addAction(exitAction)
		# toolbar.addAction(openfile)

		# btn1 = QPushButton("Button 1", self)

		# btn2 = QPushButton("Button 2", self)

		# btn1.clicked.connect(self.buttonClicked)
		# btn2.clicked.connect(self.buttonClicked)

		self.statusBar()

		self.central_widget.setLayout(grid)
		self.setCentralWidget(self.central_widget)
		self.setGeometry(300, 300, 900, 900)
		self.setWindowTitle('Sample')

		self.show()

	def buttonClicked(self):
		sender = self.sender()
		self.statusBar().showMessage(sender.text() + ' was pressed')

	def choose_file(self):
		try:
			fname = QFileDialog.getOpenFileName(self, 'open file', '/')
			self.file_path = fname[0]
			self.file_path_label.setText(fname[0])
		except IOError:
			self.statusBar().showMessage('Input Error')

	def play_sound(self):
		playsound.playsound(self.file_path)

	def record_sound(self):
		file_path = 'Output.wav'
		VoiceRecord.voice_record(file_path)
		self.file_path = file_path
		self.file_path_label.setText(self.file_path)


	def speech_to_text(self):
		r = ms.RecognizeSpeech_FromFile(self.file_path)
		K.clear_session()
		str_pinyin = r
		r = ml.SpeechToText(str_pinyin)
		return r

	def plot_recognize_result(self):
		try:
			self.statusBar().showMessage('Processing')
			pridict = self.speech_to_text()
			self.predict.setText(pridict)
			time.sleep(0.5)
		except IOError:
			self.statusBar().showMessage('No such File!')

	def plot_wave(self):
		try:
			VoiceAnalasis.generate_wave(file_path=self.file_path)
			self.png.setPixmap(QPixmap('wave.png'))

		except IOError:
			self.statusBar().showMessage('Open A File First!')

	def plot_spec(self):
		try:
			VoiceAnalasis.generate_spec(file_path=self.file_path)
			self.png.setPixmap(QPixmap('spec.png'))

		except IOError:
			self.statusBar().showMessage('Open A File First!')

	def plot_CQT(self):
		try:
			VoiceAnalasis.generate_CQT(file_path=self.file_path)
			self.png.setPixmap(QPixmap('CQT.png'))

		except IOError:
			self.statusBar().showMessage('Open A File First!')

	def plot_mfcc(self):
		try:
			VoiceAnalasis.generate_mfcc(file_path=self.file_path)
			self.png.setPixmap(QPixmap('mfcc.png'))

		except IOError:
			self.statusBar().showMessage('Open A File First!')




if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Example()

	modelpath = 'model_speech' + '\\'
	datapath = '.'
	global ms
	ms = ModelSpeech(datapath)
	ms.LoadModel(modelpath + 'speech_model251_e_0_step_625000.model')

	global ml
	ml = ModelLanguage('model_language')
	ml.LoadModel()

	sys.exit(app.exec_())
