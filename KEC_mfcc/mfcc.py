from python_speech_features import mfcc
from python_speech_features import logfbank
import scipy.io.wavfile as wav

(rate, sig) = wav.read("/home/nianheng/Documents/hiwi/02februar/fabian_mfcc/armed_original.wav")
print(len(sig))

mfcc_feat = mfcc(sig, rate, winlen=0.001, numcep=12)
fbank_feat = logfbank(sig,rate)
print(mfcc_feat)
print(len(mfcc_feat))
# print(mfcc_feat[1:13,: ])
