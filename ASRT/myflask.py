from flask import Flask
from flask import Flask,send_from_directory
from flask import request
from datetime import timedelta
import VoiceAnalasis as va
import pinyin
import tensorflow as tf
import datetime
from flask_cors import *  # 导入模块
import urllib
import keras
import os
from SpeechModel251 import ModelSpeech
from LanguageModel2 import ModelLanguage
from general_function.file_wav import *


graph = tf.get_default_graph()
datapath = './'
wavedict='C:\\Users\\17000\\AI\\ASRT\\wavdata\\'
wavelist=os.listdir(wavedict)
fname='myfname'
modelpath = 'model_speech/'
ms = ModelSpeech(datapath)
ms.LoadModel(modelpath + 'speech_model251_e_0_step_625000.model')

ml = ModelLanguage('model_language')
ml.LoadModel()

app= Flask(__name__)
app.config['JSON_AS_ASCII']=False
app.debug=True
CORS(app, supports_credentials=True)  # 设置跨域
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

mylogin='mylogin'
@app.route('/api/',methods=['GET','POST'])
def hello_world():
    if request.method== 'POST':
        return 'hello world'

@app.route('/')
@cross_origin()
def login():
    print('login')
    return send_from_directory(wavedict,filename='20170001P00001A0001.wav',as_attachment=True)

@app.route('/api/download')
@cross_origin()
def mydownload():
    print('badbadbadbad')
    global fname
    print(fname)
    return send_from_directory(wavedict,filename=fname,as_attachment=True)

@app.route('/api/plotwave')
@cross_origin()
def myplotwave():
    l=len(fname)
    pname=fname[0:l-4]+'.png'
    print(pname)
    return send_from_directory(wavedict+"wave",filename=pname,as_attachment=True)

@app.route('/api/plotspec')
@cross_origin()
def myplotspec():
    l=len(fname)
    pname=fname[0:l-4]+'.png'
    print(pname)
    return send_from_directory(wavedict+"spec",filename=pname,as_attachment=True)

@app.route('/api/plotCQT')
@cross_origin()
def myplotCQT():
    l=len(fname)
    pname=fname[0:l-4]+'.png'
    print(pname)
    return send_from_directory(wavedict+"CQT",filename=pname,as_attachment=True)

@app.route('/api/plotmfcc')
@cross_origin()
def myplotmfcc():
    l=len(fname)
    pname=fname[0:l-4]+'.png'
    print(pname)
    return send_from_directory(wavedict+"mfcc",filename=pname,as_attachment=True)

@app.route('/api/plotmfccs')
@cross_origin()
def myplotmfccs():
    l=len(fname)
    pname=fname[0:l-4]+'.png'
    print(pname)
    return send_from_directory(wavedict+"mfccs",filename=pname,as_attachment=True)

@app.route('/api/download2')
@cross_origin()
def mydownload2():
    global fname
    return send_from_directory(wavedict,filename=fname,as_attachment=True)

@app.route('/api/wavelist',methods=['GET','POST'])
def getwavelist():
    if request.method=='POST':
        wavelist=os.listdir(wavedict)
        return {'wavelist':wavelist}

@app.route('/api/changefname',methods=['GET','POST'])
def changefname():
    if request.method=='POST':
        tempdata=request.data
        tempdata=eval(tempdata)
        global fname
        fname=tempdata['fname']
        print(fname)
        return '1'

@app.route('/api/getsentence' ,methods=['GET','POST'])
def getsentence():
    if request.method=='POST':
        tempdata=request.data
        tempdata=eval(tempdata)
        global fname
        fname=tempdata['fname']
        fpath=wavedict+fname
        #print(fpath)
        wavs,fs=read_wav_data(fpath)
        #print(wavs)
        wavs=wavs.tolist()
        #print(wavs)
        #print(type(wavs))
        #print(wavs[0][0])
        #print(type(wavs[0][0]))
        #print(fs)
        #print(type(fs))
        global graph                      # 新添加的代码。。。。。。
        with graph.as_default():
            r_speech = ms.RecognizeSpeech(wavs, fs)
        print(r_speech)
        str_pinyin = r_speech
        r_speech=pinyin.process_pin_yin(r_speech)
        r = ml.SpeechToText(str_pinyin)
        l=len(fname)
        specdict=os.listdir(wavedict+"spec\\")
        if fname[0:l-4]+'.png' not in specdict:
            print("notin")
            data,sr=va.load_voice(wavedict+fname)
            va.path=wavedict
            va.plot_wave(data,sr,fname[0:l-4])
            va.plot_spec(data,sr,fname[0:l-4])
            va.plot_CQT(data, sr,fname[0:l-4])
            va.plot_mfcc(data, sr, standardize=False,title=fname[0:l-4])
            va.plot_mfcc(data, sr, standardize=True,title=fname[0:l-4])
        print(r)
        print(r_speech[0][1])
        return {
            'r':r,
            'r_speech':r_speech
        }

        



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=5000)