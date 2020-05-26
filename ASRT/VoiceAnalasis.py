import librosa  # 要求版本0.6.1
import librosa.display  # display 模块并没有被默认包含，需要额外给出
import matplotlib.pyplot as plt
import numpy as np
import sklearn


# 读取声音信息
def load_voice(file_path):
	# 使用原音频的采样信息16K进行采样
	data, sample_rate = librosa.load(file_path, sr=None)
	return data, sample_rate


# 获取声音的mfcc特征
def get_mfcc(data, sr):
	mfccs = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=40)
	return mfccs

def get_standardized_mfcc(data, sr):
	mfccs = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=40)
	mfccs = sklearn.preprocessing.scale(mfccs, axis=1)  # 需要安装库sklearn，预处理数据
	return mfccs

# 获取声音的Log-Mel Spectrogram特征
def get_logmelspec(data, sr):
	melspec = librosa.feature.melspectrogram(data, sr, n_fft=1024, hop_length=512, n_mels=128)
	logmelspec = librosa.power_to_db(melspec)
	return logmelspec


#  画波形图
def plot_wave(data, sr, title='Default'):
	thispath=path+"wave\\"
	plt.figure()
	librosa.display.waveplot(data, sr)
	plt.title(title)
	plt.savefig(thispath+title+'.png')
	plt.close()


# 画频谱图：Log-Mel Spectrogram频谱
def plot_spec(data, sr, title='Default'):
	thispath=path+"spec\\"
	logmelspec = get_logmelspec(data, sr)
	plt.figure()
	librosa.display.specshow(logmelspec, sr=sr, x_axis='time', y_axis='mel')
	plt.title(title)
	plt.colorbar(format='%+2.0f dB')
	plt.savefig(thispath+title+'.png')
	plt.close()


# 展示CQT变换
def plot_CQT(data, sr, title='Default'):
	thispath=path+"CQT\\"
	CQT = librosa.amplitude_to_db(librosa.cqt(data, sr=16000), ref=np.max)
	librosa.display.specshow(CQT, y_axis='cqt_note')
	plt.colorbar(format='%+2.0f dB')
	plt.title(title)
	plt.savefig(thispath+title+'.png')
	plt.close()


def plot_wave_spec(data, sr, title1='Default', title2='Default'):
	plt.figure(figsize=(8, 6))
	plt.subplot(2, 1, 1)
	plt.title(title1)
	librosa.display.waveplot(data, sr)
	plt.subplot(2, 1, 2)
	plt.title(title2)

	logmelspec = get_logmelspec(data, sr)
	librosa.display.specshow(logmelspec, sr=sr, x_axis='time', y_axis='mel')
	plt.colorbar(format='%+1.0f dB')
	plt.tight_layout(h_pad=0.5)
	plt.show()

# 画mfcc图
def plot_mfcc(data, sr, standardize=True, title='Default'):
	if standardize:
		thispath=path+"mfccs\\"
		plt.title(title)
		mfccs = get_standardized_mfcc(data, sr)
	else:
		thispath=path+"mfcc\\"
		plt.title(title)
		mfccs = get_mfcc(data, sr)
	librosa.display.specshow(mfccs, sr=sr, x_axis='time')
	plt.savefig(thispath+title+'.png')
	plt.close()



#f = 'C:\\Users\\17000\\AI\\ASRT_v0.6.1\\wavdata\\20170001P00001A0001.wav'
#data, sr = load_voice(f)
path='C:\\Users\\17000\\AI\\ASRT_v0.6.1\\wavdata\\'

"""
plot_wave(data, sr)
plot_spec(data, sr)
plot_CQT(data, sr)
plot_wave_spec(data, sr)
plot_mfcc(data, sr, standardize=False)
plot_mfcc(data, sr, standardize=True)
"""



