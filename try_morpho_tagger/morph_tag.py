import textgrid
import os
import glob
import shutil
import re
from RDRPOSTagger3.pSCRDRtagger import RDRPOSTagger
from RDRPOSTagger3.Utility.Utils import readDictionary

#nltk.download('punkt')
annotation = '<[A-ZÄÖÜß]*>|^$'


def get_text(tier):
    t=[]
    for i in tier:
        t.append(str(i.mark))
    annotation_map = mark_annotation_map(t)
    print('after text' + str(len(t)))
    print(t)
    return t, annotation_map




def mark_annotation_map(t):
    annotation_map = {}
    n=0
    for each_word in t:
        if re.match(annotation, each_word) is not None:
            annotation_map[n] = each_word
        n=n+1
    print('annotation_map: '+str(len(annotation_map)))
    print(annotation_map)
    return annotation_map


def run(name):
    tg=textgrid.TextGrid()
    tg.read(name)
    t_num=1
    korr = False
    for each_tier in tg.tiers:
        if (each_tier.name == 'words.korr') or (each_tier.name == "words-korr"):
            korr = True
    for each_tier in tg.tiers:
        if (each_tier.name == 'words.korr') or (each_tier.name == "words-korr"):
            t, annotation_map = get_text(each_tier)
            for word in t:
                if re.match(annotation, word) is not None:
                    t.remove(word)
            t = ' '.join(t)
            return t,t_num,each_tier.name, annotation_map
        elif (each_tier.name == 'words.corr' or each_tier.name == "words-corr") and (not korr):
            t, annotation_map = get_text(each_tier)
            for word in t:
                if (re.match(annotation, word) is not None):
                    t.remove(word)
            t = ' '.join(t)
            return t,t_num, each_tier.name, annotation_map
        else:
            t_num = t_num + 1





def tag(t):
    tagger = RDRPOSTagger.RDRPOSTagger()
    tagger.constructSCRDRtreeFromRDRfile("F:\hiwi\\09september\\try_morpho_tagger\RDRPOSTagger3\Models\MORPH\German.RDR")
    DICT = readDictionary("F:\hiwi\\09september\\try_morpho_tagger\RDRPOSTagger3\Models\MORPH\German.DICT")
    t_copy = t.split()
    print("t_copy: "+str(len(t_copy)))

    result = tagger.tagRawSentence(DICT,t)
    result_list = result.split(' ')
    print('tagged:'+str(len(result_list)))
    print(result_list)
    return result_list
    '''
    sentence = str(t)
    text = nltk.word_tokenize(sentence)
    with open('nltk_german_classifier_data.pickle', 'rb') as f:
        tagger = pickle.load(f)
    t = tagger.tag(text)
    return t
    '''




def recover(t, annotation_map):
    n = 0
    for each in t:
        position_of_slash = each.find('/')
        new_each = each[position_of_slash+1:]
        t[n] = new_each
        n = n+1
    for key in annotation_map:
        t.insert(key,annotation_map[key])
    #t = [x[1] for x in t]
    print('recovered t: '+str(len(t)))
    print(t)
    return t





def write_in_textgrid(t,name_path, t_num, tier_name):
    name = os.path.basename(name_path)
    name_new = 'new_'+name
    name_new2 = 'new2_'+name
    name_new = "F:/hiwi/09september/"+name_new
    name_new2 ="F:/hiwi/09september/"+ name_new2
    i=0
# change size
    with open(name_new,'w',encoding='utf-8') as new_f:
        with open (name_path,encoding='utf-8') as old_f:
            for line in old_f:
                if  line.strip() == "size = 2":
                    new_f.write(line.replace('size = 2', 'size = 3') + '\r')
                    total_t_num = 3
                elif line.strip() == "size = 3":
                    new_f.write(line.replace('size = 3', 'size = 4') + '\r')
                    total_t_num = 4
                elif line.strip() == "size = 1":
                    new_f.write(line.replace('size = 1', 'size = 2') + '\r')
                    total_t_num = 2
                else:
                    new_f.write(line)
    #copy the tier
    with open(name_new,'r+',encoding='utf-8') as infile, open (name_new2, 'w',encoding='utf-8') as outfile:
        copy = False
        for line in infile:
            if line.strip() == 'item ['+str(t_num)+']:':
                line = 'item ['+str(total_t_num)+']:' + '\r'
                outfile.write(line)
                copy = True
            elif line.strip() =='name = "'+tier_name+'"':
                line = 'name = "morph-tag"' + '\r'
                outfile.write(line)
                copy = True
            elif line.strip() == 'item [' +str(t_num+1)+ ']:':
                break
            elif copy:
                outfile.write(line)
    outfile.close()
    #change text of the copied tier
    with open(name_new2,'r+',encoding='utf-8') as infile, open (name_new, 'a',encoding='utf-8') as outfile:
        for line in infile:
            if "text =" in line:
                line = "            text = " + '"'+str(t[i])+'"' + '\r'
                outfile.write(line)
                i = i+1
            else:
                outfile.write(line)
    move_name = os.path.basename(name_new)
    dst = "F:/hiwi/09september/TextGrids_change_encoding_morphtag/" + move_name
    shutil.move(name_new, dst)
    os.remove(name_new2)






def name():
    '''
    get names of all files
    :return: path_list: path+name of files
    '''

    path_list=glob.glob("F:\hiwi\\09september\\TextGrids_change_encoding"+"\*.TextGrid")
    return path_list





if __name__ == '__main__':

    name_list = name()
    n = len(name_list)-1
    while n>=0:
        print(name_list[n])
        t, t_num, tier_name, annotation_map = run(name_list[n])
        t = tag(t)
        t = recover(t, annotation_map)
        write_in_textgrid(t,name_list[n],t_num, tier_name)
        n=n-1
