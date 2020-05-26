from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QToolTip, \
	QAction, qApp, QTextEdit, QWidget, QFileDialog, QLabel, QGridLayout
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QFont

import simpleaudio
import VoiceAnalasis
import VoiceRecord
import sys, time

from SpeechModel251 import ModelSpeech
from LanguageModel2 import ModelLanguage
from keras import backend as K


class Window(QMainWindow):

	def __init__(self):
		super().__init__()
		self.central_widget = QWidget()
		self.file_label = QLabel('File path')
		self.file_path_label = QLabel('N/A')
		self.pin_yin_label = QLabel('Spell')
		self.pin_yin_result_label = QLabel('N/A')
		self.result_label = QLabel('Result')
		self.predict = QLabel('N/A')
		self.picture_label = QLabel('Analasis Pictures')
		self.png = QLabel('Picture')

		self.set_label_style()
		self.file_path = ''
		self.d = dict()
		self.init_pin_yin()
		self.initUI()


	def set_label_style(self):
		self.file_label.setStyleSheet("font-size:28px;font-weight:normal;font-family:Consolas;}")
		self.file_path_label.setStyleSheet("font-size:28px;font-weight:normal;font-family:Consolas;}")
		self.pin_yin_label.setStyleSheet("font-size:28px;font-weight:normal;font-family:Consolas;}")
		self.pin_yin_result_label.setStyleSheet("font-size:28px;font-weight:normal;font-family:Consolas;}")
		self.result_label.setStyleSheet("font-size:28px;font-weight:normal;font-family:Consolas;}")
		self.predict.setStyleSheet("font-size:28px;font-weight:normal;font-family:Consolas;}")
		self.picture_label.setStyleSheet("font-size:28px;font-weight:normal;font-family:Consolas;}")

	def initUI(self):

		QToolTip.setFont(QFont('SansSerif', 16))
		# 退出函数
		exitAction = QAction('&Exit', self)
		exitAction.setShortcut('Ctrl+0')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(qApp.quit)

		# 打开文件
		openfile = QAction('Open', self)
		openfile.setShortcut('Ctrl+1')
		openfile.setStatusTip('Open new file')
		openfile.triggered.connect(self.choose_file)

		# 播放原语音
		playsound = QAction('Play sound', self)
		playsound.setShortcut('Ctrl+2')
		playsound.setStatusTip('Play original Sound')
		playsound.triggered.connect(self.play_sound)

		# 录制声音
		recordsound = QAction('Record sound', self)
		recordsound.setShortcut('Ctrl+3')
		recordsound.setStatusTip('Record a wav sound file for 8 seconds')
		recordsound.triggered.connect(self.record_sound)

		# 识别语音
		recognizefile = QAction('Recognize', self)
		recognizefile.setShortcut('Ctrl+4')
		recognizefile.setStatusTip('Recognize the File you just open')
		recognizefile.triggered.connect(self.plot_recognize_result)

		# 生成wave.png
		get_wave = QAction('Get wave', self)
		get_wave.setShortcut('Ctrl+5')
		get_wave.setStatusTip('Generate WAVE plot for the chosen voice')
		get_wave.triggered.connect(self.plot_wave)

		# spec.png
		get_spec = QAction('Get spec', self)
		get_spec.setShortcut('Ctrl+6')
		get_spec.setStatusTip('Generate SPEC plot for the chosen voice')
		get_spec.triggered.connect(self.plot_spec)

		# CQT.png
		get_CQT = QAction('Get CQT', self)
		get_CQT.setShortcut('Ctrl+7')
		get_CQT.setStatusTip('Generate CQT plot for the chosen voice')
		get_CQT.triggered.connect(self.plot_CQT)

		# mfcc.png
		get_mfcc_normal = QAction('Get MFCC Normal', self)
		get_mfcc_normal.setShortcut('Ctrl+8')
		get_mfcc_normal.setStatusTip('Generate Normal MFCC plot for the chosen voice')
		get_mfcc_normal.triggered.connect(self.plot_mfcc_normal)

		get_mfcc_std = QAction('Get MFCC Stadardized', self)
		get_mfcc_std.setShortcut('Ctrl+9')
		get_mfcc_std.setStatusTip('Generate Stadardized MFCC plot for the chosen voice')
		get_mfcc_std.triggered.connect(self.plot_mfcc_std)
		# 文本框

		# 布局

		grid = QGridLayout()
		grid.setSpacing(50)
		# QWidget* widget, int fromRow, int fromColumn, int rowSpan, int columnSpan, Qt::Alignment alignment = 0
		grid.addWidget(self.file_label, 0, 0)
		grid.addWidget(self.file_path_label, 0, 1)
		grid.addWidget(self.pin_yin_label, 1, 0)
		grid.addWidget(self.pin_yin_result_label, 1, 1)
		grid.addWidget(self.result_label, 2, 0)
		grid.addWidget(self.predict, 2, 1)
		grid.addWidget(self.picture_label, 3, 0)
		grid.addWidget(self.png, 3, 1)
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
		picMenu.addAction(get_mfcc_normal)
		picMenu.addAction(get_mfcc_std)
		# toolbar = self.addToolBar('&Exit')
		# toolbar.addAction(exitAction)
		# toolbar.addAction(openfile)

		# btn1 = QPushButton("Button 1", self)

		# btn2 = QPushButton("Button 2", self)

		# btn1.clicked.connect(self.buttonClicked)
		# btn2.clicked.connect(self.buttonClicked)

		self.png.setPixmap(QPixmap('Blank.png'))

		self.statusBar()

		self.central_widget.setLayout(grid)
		self.setCentralWidget(self.central_widget)
		self.setGeometry(300, 300, 1200, 900)
		self.setWindowTitle('Sample')

		self.show()


	def choose_file(self):
		try:
			fname = QFileDialog.getOpenFileName(self, 'open file', '/')
			self.file_path = fname[0]
			self.file_path_label.setText(fname[0])
			self.predict.setText('N/A')
			self.pin_yin_result_label.setText('N/A')
			self.png.setPixmap(QPixmap('Blank.png'))
		except IOError:
			self.statusBar().showMessage('Input Error')

	def play_sound(self):
		wave_obj = simpleaudio.WaveObject.from_wave_file(self.file_path)
		play_obj = wave_obj.play()
		play_obj.wait_done()  # 等到声音播放完毕

	def tmp(self, str):
		self.statusBar().showMessage(str)

	def record_sound(self):
		file_path = 'Output.wav'
		self.statusBar().showMessage('Now recording')
		VoiceRecord.voice_record(file_path)
		self.file_path = file_path
		self.statusBar().showMessage('Record finished')
		self.file_path_label.setText(self.file_path)
		self.predict.setText('N/A')
		self.pin_yin_result_label.setText('N/A')
		self.png.setPixmap(QPixmap('Blank.png'))

	def speech_to_text(self):
		r = ms.RecognizeSpeech_FromFile(self.file_path)
		K.clear_session()
		str_pinyin = r
		record = str_pinyin
		r = ml.SpeechToText(str_pinyin)
		return record, r

	def plot_recognize_result(self):
		try:
			self.statusBar().showMessage('Processing')
			pin_yin, pridict = self.speech_to_text()
			pin_yin = self.process_pin_yin(pin_yin)
			pin_yin = ' '.join(pin_yin)
			self.pin_yin_result_label.setText(pin_yin)
			self.predict.setText(pridict)
		except IOError:
			self.statusBar().showMessage('No such File!')

	def init_pin_yin(self):
		self.d[('a', 1)], self.d[('a', 2)], self.d[('a', 3)], self.d[('a', 4)], self.d[('a', 5)] = 'ā', 'á', 'ǎ', 'à', 'a'
		self.d[('o', 1)], self.d[('o', 2)], self.d[('o', 3)], self.d[('o', 4)], self.d[('o', 5)] = 'ō', 'ó', 'ǒ', 'ò', 'o'
		self.d[('e', 1)], self.d[('e', 2)], self.d[('e', 3)], self.d[('e', 4)], self.d[('e', 5)] = 'ē', 'é', 'ě', 'è', 'e'
		self.d[('i', 1)], self.d[('i', 2)], self.d[('i', 3)], self.d[('i', 4)], self.d[('i', 5)] = 'ī', 'í', 'ǐ', 'ì', 'i'
		self.d[('u', 1)], self.d[('u', 2)], self.d[('u', 3)], self.d[('u', 4)], self.d[('u', 5)] = 'ū', 'ú', 'ǔ', 'ù', 'u'
		self.d[('v', 1)], self.d[('v', 2)], self.d[('v', 3)], self.d[('v', 4)], self.d[('v', 5)] = 'ǖ', 'ǘ', 'ǚ', 'ǜ', 'v'

	def process_pin_yin(self, pin_yin):
		ans = []
		for word in pin_yin:
			tune = int(word[-1])
			if word.find('a') != -1:
				loc = word.find('a')
				word = word[0: loc] + self.d[('a', tune)] + word[loc + 1: -1]
			elif word.find('o') != -1:
				loc = word.find('o')
				word = word[0: loc] + self.d[('o', tune)] + word[loc + 1: -1]
			elif word.find('e') != -1:
				loc = word.find('e')
				word = word[0: loc] + self.d[('e', tune)] + word[loc + 1: -1]
			elif word.find('i') != -1:
				loc = word.find('i')
				word = word[0: loc] + self.d[('i', tune)] + word[loc + 1: -1]
			elif word.find('u') != -1:
				loc = word.find('u')
				word = word[0: loc] + self.d[('u', tune)] + word[loc + 1: -1]
			elif word.find('v') != -1:
				loc = word.find('v')
				word = word[0: loc] + self.d[('v', tune)] + word[loc + 1: -1]
			ans.append(word)
		return ans

	def plot_wave(self):
		try:
			VoiceAnalasis.generate_wave(file_path=self.file_path)
			self.png.setPixmap(QPixmap('wave.png'))
			self.statusBar().showMessage('Finished')

		except IOError:
			self.statusBar().showMessage('Open A File First!')

	def plot_spec(self):
		try:
			VoiceAnalasis.generate_spec(file_path=self.file_path)
			self.png.setPixmap(QPixmap('spec.png'))
			self.statusBar().showMessage('Finished')
		except IOError:
			self.statusBar().showMessage('Open A File First!')

	def plot_CQT(self):
		try:
			self.statusBar().showMessage('Processing')
			VoiceAnalasis.generate_CQT(file_path=self.file_path)
			self.png.setPixmap(QPixmap('CQT.png'))
			self.statusBar().showMessage('Finished')

		except IOError:
			self.statusBar().showMessage('Open A File First!')

	def plot_mfcc_normal(self):
		try:
			VoiceAnalasis.generate_mfcc(file_path=self.file_path, standardize=False)
			self.png.setPixmap(QPixmap('mfcc.png'))
			self.statusBar().showMessage('Finished')

		except IOError:
			self.statusBar().showMessage('Open A File First!')

	def plot_mfcc_std(self):
		try:
			VoiceAnalasis.generate_mfcc(file_path=self.file_path)
			self.png.setPixmap(QPixmap('mfcc.png'))
			self.statusBar().showMessage('Finished')

		except IOError:
			self.statusBar().showMessage('Open A File First!')




if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Window()

	modelpath = 'model_speech' + '\\'
	datapath = '.'
	global ms
	ms = ModelSpeech(datapath)
	ms.LoadModel(modelpath + 'speech_model251_e_0_step_625000.model')

	global ml
	ml = ModelLanguage('model_language')
	ml.LoadModel()

	sys.exit(app.exec_())
