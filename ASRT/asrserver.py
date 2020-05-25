#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nl8590687
语音识别API的HTTP服务器程序

"""
import http.server
import urllib
import keras
import os
from SpeechModel251 import ModelSpeech
from LanguageModel2 import ModelLanguage
from general_function.file_wav import *

datapath = './'
wavedict='C:\\Users\\17000\\AI引论语音识别\\ASRT_v0.6.1\\wavdata\\'
wavelist=os.listdir(wavedict)
modelpath = 'model_speech/'
ms = ModelSpeech(datapath)
ms.LoadModel(modelpath + 'speech_model251_e_0_step_625000.model')

ml = ModelLanguage('model_language')
ml.LoadModel()

class TestHTTPHandle(http.server.BaseHTTPRequestHandler):  
	def setup(self):
		self.request.settimeout(10)
		http.server.BaseHTTPRequestHandler.setup(self)
	
	def _set_response(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()
		
	def do_GET(self):  
	
		buf = 'ASRT_SpeechRecognition API'  
		self.protocal_version = 'HTTP/1.1'   
		
		self._set_response()
		
		buf = bytes(buf,encoding="utf-8")
		self.wfile.write(buf) 
		
	def do_POST(self):  
		'''
		处理通过POST方式传递过来并接收的语音数据
		通过语音模型和语言模型计算得到语音识别结果并返回
		'''
		selectedwave=wavedict+wavelist[0]
		path = self.path  
		print(path)  
		print(self.headers)
		#获取post提交的数据  
		datas = self.rfile.read(int(self.headers['content-length']))  
		#datas = urllib.unquote(datas).decode("utf-8", 'ignore') 
		datas = datas.decode('utf-8')
		#print('datas')
		#print(datas)
		datas=eval(datas)
		#datas_split = datas.split('&')
		token=datas['token']
		if	token == 'qwertasd':
			print('selectedwave')
			print(selectedwave)
			wavs,fs=read_wav_data(selectedwave)
			#wavs,fs=read_wav_data(datas['fname'])
			#wavs,fs=read_wav_data('E:\\sbz\\Documents\\speechrecognition\\speech\\datalist\\ST-CMDS-20170001_1-OS\\20170001P00001A0001.wav')
			#mydatas={'token':token, 'fs':fs, 'wavs':wavsignal}
			#datas_split = mydatas.split('&')
			#type = 'wavfilebytes' # wavfilebytes or python-list

			# for line in datas_split:
			# 	[key, value]=line.split('=')
			# 	if('wavs' == key and '' != value):
			# 		wavs.append(int(value))
			# 	elif('fs' == key):
			# 		fs = int(value)
			# 	elif('token' == key ):
			# 		token = value
			# 	#elif('type' == key):
			# 	#	type = value
			# 	else:
			# 		print(key, value)
			print('wavs')
			print(wavs)	
			if(token != 'qwertasd'):
				buf = '403'
				print(buf)
				buf = bytes(buf,encoding="utf-8")
				self.wfile.write(buf)  
				return

			#if('python-list' == type):
			if(len(wavs)>0):
				r = self.recognize(wavs, fs)
			else:
				r = ''
			#else:
			#	r = self.recognize_from_file('')

			if(token == 'qwertasd'):
			#buf = '成功\n'+'wavs:\n'+str(wavs)+'\nfs:\n'+str(fs)
				buf = r
			else:
				buf = '403'
		
		#print(datas)
		
		if token == 'wl':
			buf=wavelist

		print(token)
		self._set_response()
		
		#buf = '<!DOCTYPE HTML> \n<html> \n<head>\n<title>Post page</title>\n</head> \n<body>Post Data:%s  <br />Path:%s\n</body>  \n</html>'%(datas,self.path)  
		print(buf)
		buf = bytes(buf,encoding="utf-8")
		self.wfile.write(buf)  
		
	def recognize(self, wavs, fs):
		r=''
		try:
			r_speech = ms.RecognizeSpeech(wavs, fs)
			print(r_speech)
			str_pinyin = r_speech
			r = ml.SpeechToText(str_pinyin)
		except:
			r=''
			print('[*Message] Server raise a bug. ')
		return r
		pass
	
	def recognize_from_file(self, filename):
		pass

import socket

class HTTPServerV6(http.server.HTTPServer):
	address_family = socket.AF_INET6

def start_server(ip, port):  
	
	if(':' in ip):
		http_server = HTTPServerV6((ip, port), TestHTTPHandle)
	else:
		http_server = http.server.HTTPServer((ip, int(port)), TestHTTPHandle)
	
	print('服务器已开启')
	
	try:
		http_server.serve_forever() #设置一直监听并接收请求  
	except KeyboardInterrupt:
		pass
	http_server.server_close()
	print('HTTP server closed')
	
if __name__ == '__main__':
	start_server('', 20000) # For IPv4 Network Only
	#start_server('::', 20000) # For IPv6 Network
	
	
	
	
