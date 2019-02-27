import os
import textgrid
from pydub import AudioSegment
import re


annotation = '<[A-ZÄÖÜß]*>|^$'

def read_file_names(path):
    file_list = os.listdir(path)
    return file_list


def read_text_grid(name):
    tg=textgrid.TextGrid()
    tg.read(name)
    korr = False
    for each_tier in tg.tiers:
        if (each_tier.name == 'words.korr') or (each_tier.name == "words-korr"):
            korr = True
    for each_tier in tg.tiers:
        if (each_tier.name == 'words.korr') or (each_tier.name == "words-korr"):
            phrase_list = get_text(each_tier)
            return phrase_list
        elif (each_tier.name == 'words.corr' or each_tier.name == "words-corr") and (not korr):
            phrase_list = get_text(each_tier)
            return phrase_list




def get_text(tier):

    phrase_list =[]
    intervals = tier.intervals
    new_phrase = None

    for each_word in intervals:

        if re.match(annotation, each_word.mark) is not None:

            if new_phrase is not None:
                phrase_list.append(new_phrase)

            new_phrase = phrase(each_word.minTime, each_word.maxTime)
            new_phrase.append_string(each_word.mark)
            phrase_list.append(new_phrase)
            new_phrase = None

        else:
            each_word_mark = clean_word(each_word.mark)
            if new_phrase is not None:
                new_phrase.append_string(each_word_mark)
                new_phrase.update_end_time(each_word.maxTime)
            else:
                new_phrase = phrase(each_word.minTime, each_word.maxTime)
                new_phrase.append_string(each_word_mark)

    if new_phrase is not None:
        phrase_list.append(new_phrase)

    return phrase_list




class phrase:
    def __init__(self, start_time, end_time):
        self.start_time = start_time
        self.end_time = end_time
        self.string_list = []

    def append_string (self, new_word):
        self.string_list.append(new_word)

    def get_string (self):
        a_string = " ".join(self.string_list)
        return a_string

    def update_end_time (self, new_end_time):
        self.end_time = new_end_time




def strip_txt_and_wav (phrase_list, wav_path, empty_path, none_empty_path, filename):
    filename = filename[:-9]
    suffix = 0
    this_whole_wav = AudioSegment.from_wav(wav_path + filename + ".wav")
    for each_phrase in phrase_list:
        phrase_string = each_phrase.get_string()
        if re.match(annotation, phrase_string) is not None:
            with open(empty_path+filename+"_"+str(suffix)+".txt", 'w') as file:
                file.write(phrase_string)
            this_wav = this_whole_wav[int(each_phrase.start_time* 1000) : int(each_phrase.end_time *1000)]
            this_wav.export(empty_path+filename+"_"+str(suffix)+".wav", format="wav")
            suffix += 1

        else:
            with open(none_empty_path+filename+"_"+str(suffix)+".txt", 'w') as file:
                file.write(phrase_string)
            this_wav = this_whole_wav[int(each_phrase.start_time * 1000) : int(each_phrase.end_time * 1000)]
            this_wav.export(none_empty_path + filename + "_" + str(suffix) + ".wav", format="wav")
            suffix += 1



def clean_word(word_string):
    word_string = word_string.replace("ä", "ae")
    word_string = word_string.replace("ö", "oe")
    word_string = word_string.replace("ü", "ue")
    word_string = word_string.replace("ß", "ss")
    word_string = word_string.replace("Ä", "Ae")
    word_string = word_string.replace("Ö", "Oe")
    word_string = word_string.replace("Ü", "Ue")
    return word_string



if __name__ == '__main__':
    textgrid_path = "/home/nianheng/Documents/hiwi/12December/Nianheng_Fabian/TextGrids_problem/"
    audio_path = "/home/nianheng/Documents/hiwi/12December/Nianheng_Fabian/Wav_processed_no_names/"
    #textgrid_path = "/home/nianheng/Documents/hiwi/12December/Nianheng_Fabian/test/text/"
    #audio_path = "/home/nianheng/Documents/hiwi/12December/Nianheng_Fabian/test/wav/"
    empty_path = "/home/nianheng/Documents/hiwi/12December/Nianheng_Fabian/step1_aligner/empty/"
    none_empty_path = "/home/nianheng/Documents/hiwi/12December/Nianheng_Fabian/step1_aligner/none_empty/"

    textgrid_file_name = read_file_names(textgrid_path)
    audio_file_name = read_file_names(audio_path)

    for each_file_name in textgrid_file_name:
        try:
            phrase_list = read_text_grid(textgrid_path+each_file_name)
            strip_txt_and_wav(phrase_list, audio_path, empty_path, none_empty_path, each_file_name)
        except Exception as e:
            print(each_file_name)
            print(str(e))



