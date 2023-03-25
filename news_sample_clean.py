import cleantext
import matplotlib.pyplot as plt
import csv
import copy

raw_data = []


with open('news_sample.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        raw_data.append(row)     

def toke_text(text):
    toke_d = text
    for i in range(len(toke_d)):
        ##text[i]['type'] = text[i]['type']
        toke_d[i]['content'] = cleantext.clean_words(toke_d[i]['content'],
                                            clean_all = False,
                                            lowercase=True,
                                            reg = r'http\S+',
                                            reg_replace = 'URL',
                                            punct=True)                               
    return toke_d

def toke_text_remStopW(text):
    toke_d = text
    for i in range(len(toke_d)):
        ##text[i]['type'] = text[i]['type']
        toke_d[i]['content'] = cleantext.clean_words(toke_d[i]['content'],
                                            clean_all = False,
                                            stopwords=True,
                                            lowercase=True,
                                            reg = r'http\S+',
                                            reg_replace = 'URL',
                                            punct=True
                                            )                               
    return toke_d

def toke_text_stem(text):
    toke_d = {}
    for i in range(len(text)):
        ##text[i]['type'] = text[i]['type']
        text[i]['content'] = cleantext.clean_words(text[i]['content'],
                                            clean_all = False,
                                            stopwords=True,
                                            lowercase=True,
                                            stemming=True,
                                            reg = r'http\S+',
                                            reg_replace = 'URL',
                                            punct=True
                                            )                               
    return text

raw2_data = copy.deepcopy(raw_data)
raw3_data = copy.deepcopy(raw_data)

toked= toke_text(raw_data)
tokedStoped=toke_text_remStopW(raw2_data)
toked_stemd_stoped = toke_text_stem(raw3_data)

def wordcount(text):
    wordcount = {}
    for i in range(len(text)):
        for word in text[i]['content']:
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
    return wordcount

toked_WC = wordcount(toked)
tokedStoped_WC = wordcount(tokedStoped)
toked_stemd_stoped_WC = wordcount(toked_stemd_stoped)

print("toked_WC:",len(toked_WC))
print("tokedStoped_WC:",len(tokedStoped_WC))
print("toked_stemd_stoped_WC:",len(toked_stemd_stoped_WC))


