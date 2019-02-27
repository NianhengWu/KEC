from python_speech_features import mfcc
import scipy.io.wavfile as wav
import textgrid
import os, re, csv
from decimal import Decimal

pattern = '<[a-zA-ZäüößÄÖÜẞ]+>'


def read_textgrid(filename):
    textgrid_obj = textgrid.TextGrid.fromFile(path + filename + '.TextGrid')
    tier = textgrid_obj.tiers[0]
    intervals = tier.intervals
    for each in intervals:
        word = each.mark
        if re.match(pattern, word) is None:
            start_time = each.minTime
            end_time = each.maxTime
            mfcc_matrix = mfcc_calculation(start_time, end_time, filename)
            with open(out, 'a+', encoding='utf8')as out_file:
                writer = csv.writer(out_file, delimiter=',')
                for i, mfcc_features in enumerate(mfcc_matrix):
                    mfcc_start_time = start_time + Decimal(i*0.01)
                    if i == len(mfcc_matrix)-1:
                        mfcc_end_time = end_time
                    else:
                        mfcc_end_time = start_time + Decimal((i+1)*0.01)
                    line = list([filename, word, start_time, end_time, mfcc_start_time, mfcc_end_time])
                    for each in mfcc_features:
                        line.append(each)
                    writer.writerow(line)
        if re.match(pattern, word) is not None:
            start_time = each.minTime
            end_time = each.maxTime
            with open(out, 'a+', encoding='utf8')as out_file:
                writer = csv.writer(out_file, delimiter=',')
                line = list([filename, word, start_time, end_time])
                writer.writerow(line)


def mfcc_calculation(s_time, e_time, filename):
    (rate, sig) = wav.read(path + filename + '.wav')
    sig_start = s_time * rate
    sig_end = e_time * rate
    sig = sig[int(sig_start):int(sig_end)]
    mfcc_feat = mfcc(sig, rate, winlen=0.01, numcep=12)
    return mfcc_feat


if __name__ == '__main__':
    path = '/home/nianheng/Documents/hiwi/02februar/fabian_mfcc/'
    out = '/home/nianheng/Documents/hiwi/02februar/KEC_mfcc.csv'
    files = os.listdir(path)

    textgrid_files = []
    for each in files:
        if each.endswith('.TextGrid'):
            textgrid_files.append(each[:-9])

    for each in textgrid_files:
        read_textgrid(each)
