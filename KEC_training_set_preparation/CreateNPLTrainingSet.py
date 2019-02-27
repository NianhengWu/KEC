import pandas as pd
import numpy as np
import textgrid
import os
import re, sys

pattern = "([A-Za-z0-1@]+[A-Za-z0-1@]+)"

def read_sentences(rootpath):
    file_list = os.listdir(rootpath)
    return file_list

class Sentences:

    def __init__(self):
        self.word_list = []

    def read_from_textgrid(self, file_textgrid_obj):
        '''
        Assume: a loads of textgrids in a path, each of which has a 'words' tier and a 'segments' tier.
                Segments tier includes all segments of every word in SAMPA.
        Read all textgrids files one by one. Read every segment corresponding to certain word and output
        infomation about this word into csv. Information including: starting/ending time, word, segments of
        the word, starting/ending time of this segment.
        :param file_list: all files in the path
        :return: nothing
        '''
        global intervals_words, intervals_segments

        tier_list = file_textgrid_obj.tiers
        interval_num = 0

        for each_tier in tier_list:
            if each_tier.name == 'words':
                tier_words = each_tier
                intervals_words = tier_words.intervals
            elif each_tier.name == 'segments':
                tier_segments = each_tier
                intervals_segments = tier_segments.intervals
                #get segments & words intervals in list
        try:
            for each_word in intervals_words:
                word_start_time = each_word.minTime
                word_end_time = each_word.maxTime
                word_mark = each_word.mark
                segment_list=[]

                a_word = Word(word_start_time, word_end_time, word_mark, segment_list)
                try:
                    while (intervals_segments[interval_num].minTime >= word_start_time) \
                            & (intervals_segments[interval_num].maxTime <= word_end_time) \
                            & (intervals_segments[interval_num].minTime != intervals_segments[interval_num].maxTime):

                        segment_mark = intervals_segments[interval_num].mark
                        m = re.match(pattern, segment_mark)
                        if m:
                            tmp_list = list(segment_mark)
                            for each_seg in tmp_list:
                                segment_list.append(each_seg)
                                #print(each_seg)
                        else:
                            segment_list.append(segment_mark)
                        interval_num += 1
                except IndexError:
                    interval_num = 0
                a_word.update_segment_list(segment_list)
                self.word_list.append(a_word)
        except AttributeError:
            print('tier words is empty or does not exist ')

class Word:
    def __init__(self, word_start_time, word_end_time, word_mark, segment_list):
        self.word_mark = word_mark
        self.word_start_time = word_start_time
        self.word_end_time = word_end_time
        self.segment_list = segment_list
        self.event_list = []
        self.num_in_event_list = 0
        self.cues_list = []

    def update_segment_list(self, new_segment_list):
        self.segment_list = new_segment_list

    def update_event_list (self, new_event_list):
        self.event_list = new_event_list

    def update_num_in_event_list(self, new_num_in_event_list):
        self.num_in_event_list = new_num_in_event_list

    def update_cues_list (self, new_cues_list):
        self.cues_list = new_cues_list

def create_event(a_sentence, filename):

    word_obj_list = a_sentence.word_list
    length = len(word_obj_list)
    event_list = []
    each_event_list = []

    for each_word in word_obj_list:
        #print(str(each_word.segment_list)+" "+each_word.word_mark)
        if each_word.word_mark != '<P>':
            each_event_list.append(each_word)
        else:
            if each_event_list != []:
                event_list.append(each_event_list)
                each_event_list = []
            else:
                each_event_list = []
    if each_event_list != []:
        event_list.append(each_event_list)

    #print(event_list)
    count_event =0
    count_word = 0
    num_in_event_list = 0


    for each_word in word_obj_list:
        if each_word.word_mark != '<P>':
            each_word.update_event_list(event_list[count_event])
            each_word.update_num_in_event_list(num_in_event_list)
            num_in_event_list += 1
            count_word += 1
        else:
            if count_word != 0 :
                #print(filename+str(count_word)+" "+str(len(word_obj_list)-1))

                if ((count_word+1) <= (len(word_obj_list)-1)):
                    if (word_obj_list[count_word+1].word_mark != '<P>'):
                        count_event += 1
                        count_word += 1
                        num_in_event_list = 0
                    else:
                        count_word += 1
                        num_in_event_list = 0

                else:
                    count_event += 1
                    count_word += 1
                    num_in_event_list = 0

            elif count_word == 0:
                count_word += 1
                num_in_event_list = 0

        #print(each_word.word_mark+" "+str(each_word.event_list) + " "+str(each_word.num_in_event_list))


def create_cues(a_sentence, existing_np, filename):
    word_obj_list = a_sentence.word_list
    df = existing_np
    for each_word in word_obj_list:
        cue_word_list = []
        cue_segment_list = []
        if each_word.word_mark != '<P>':
            event_list = each_word.event_list
            length = len(event_list)
            num_in_event_list = each_word.num_in_event_list
            if 0 <= each_word.num_in_event_list -2:
                cue_word_list.append(event_list[num_in_event_list-2])

            if 0 <= each_word.num_in_event_list -1:
                cue_word_list.append(event_list[num_in_event_list-1])

            cue_word_list.append(each_word)

            if each_word.num_in_event_list+1 <= length-1:
                cue_word_list.append(event_list[num_in_event_list+1])

            if each_word.num_in_event_list+2 <= length-1:
                cue_word_list.append(event_list[num_in_event_list+2])

            if cue_word_list[0].num_in_event_list -1 >= 0:
                vor_word = event_list[cue_word_list[0].num_in_event_list -1]
                vor_segment = vor_word.segment_list[len(vor_word.segment_list)-1]
                cue_segment_list.append(vor_segment)
            else:
                cue_segment_list.append("#")

            for each_cue_word in cue_word_list:
                for each_cue_segment in each_cue_word.segment_list:
                    cue_segment_list.append(each_cue_segment)

            if cue_word_list[len(cue_word_list)-1].num_in_event_list +1 <= len(event_list) -1:
                nach_word = event_list[cue_word_list[len(cue_word_list)-1].num_in_event_list +1]
                #print(nach_word.segment_list)
                try:
                    nach_segment = nach_word.segment_list[0]
                    cue_segment_list.append(nach_segment)
                except IndexError:
                    print(filename)
            else:
                cue_segment_list.append("#")
            #print(cue_segment_list)

            whole_cue = []

            for each_cue_word in cue_word_list:
                whole_cue.append(each_cue_word.word_mark)
                whole_cue.append("_")

            length = len(cue_segment_list)
            count = 0

            for each_cue_segment in cue_segment_list:
                if count == 0:
                    whole_cue.append(each_cue_segment)
                    whole_cue.append(cue_segment_list[count + 1])
                    whole_cue.append("_")
                    count += 1

                elif count == length - 2:
                    whole_cue.append(each_cue_segment)
                    whole_cue.append(cue_segment_list[count + 1])
                    count += 1

                elif count == length - 1:
                    break

                else:
                    whole_cue.append(each_cue_segment)
                    whole_cue.append(cue_segment_list[count + 1])
                    whole_cue.append("_")
                    count += 1

            df = write_into_df (a_sentence, each_word, whole_cue, df, filename)

    return df




def write_into_df (a_sentence, each_word, whole_cue, existing_np, filename):
    sentence = []
    event = []
    for each_word_obj in a_sentence.word_list:
        sentence.append(each_word_obj.word_mark)

    for each_word_obj in each_word.event_list:
        event.append(each_word_obj.word_mark)

    sentence_str = " ".join(sentence)
    event_str = " ".join(event)
    this_word_str = each_word.word_mark
    cue_str = "".join(whole_cue)

    new_np = np.array([[sentence_str,event_str,cue_str, this_word_str, filename]])
    results_np = np.vstack([existing_np,new_np])
    #existing_np.append([[sentence_str,event_str,cue_str, this_word_str]], axis = 0)
    #print(new_np)
    return results_np




if __name__ == '__main__':
#"/home/nianheng/Desktop/problem/0/"
    rootpath = '/home/nianheng/Documents/hiwi/10october/SWG/results_without_namefolder/'
    outpath = "/home/nianheng/Documents/hiwi/11november/"
    file_list = read_sentences(rootpath)

    df = np.array([['sentences', 'event', 'cues', 'outcomes(variant)', 'filename']])

    for each_file_name in file_list:
        file_path = rootpath + each_file_name
        try:
            file_textgrid_obj = textgrid.TextGrid.fromFile(file_path)
            a_sentence = Sentences()
            a_sentence.read_from_textgrid(file_textgrid_obj)
            create_event(a_sentence, each_file_name)
            df_np = create_cues(a_sentence,df, each_file_name)
            df = pd.DataFrame(df_np, columns=['sentences', 'event', 'cues', 'outcomes(variant)', 'filename'])
        except UnicodeDecodeError:
            print(each_file_name + ': the encode is weird, not utf-8 or ansi')
    df.to_csv(outpath + "first_try.csv", sep=",")