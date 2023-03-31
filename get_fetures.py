import os
import csv
from transformers import pipeline

words_file = 'dfs.csv'
tokens_folder = 'numerated/'
output_folder = 'features/'

model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"
sentiment_task = pipeline("sentiment-analysis", model=model_path, tokenizer=model_path)

csv.field_size_limit(1310720)

os.makedirs(output_folder, exist_ok=True)

word_id_dict = {}
header = True
with open(words_file, 'r') as f:
    reader = csv.reader(f)
    if header:
        next(reader)
    for row in reader:
        word_id_dict[row[0]] = len(word_id_dict)

def lix(article):
    '''
    Takes a string (one article) as input and returns a float.
    '''
    words = article.split()
    word_count = len(words)
    long_words = 0
    for word in words:
        if len(word) > 6:
            long_words += 1
    return long_words / word_count

def percent_in_bag(article):
    '''
    Takes a string (one article) as input and returns a float.
    '''
    words = article.split()
    word_count = len(words)
    in_bag = 0
    for word in words:
        if word in word_id_dict:
            in_bag += 1
    return in_bag / word_count

def get_sentiment(article):
    article = ' '.join(article.split()[:50]) # Maximum length of words that the model can take
    return sentiment_task(article)[0]['score']

def process(folder):
    print('Processing ' + folder)
    with open(folder, 'r') as f:
        with open(output_folder + 'features_' + folder.split('/')[-1], 'w') as g:
            reader = csv.reader(f)
            writer = csv.writer(g)
            writer.writerow(['article_id','label', 'lix', 'percent_in_bag', 'sentiment'])
            for n, row in enumerate(reader):
                print(n, end='\r')
                article_id = row[0]
                label = row[1]
                article = row[2]
                try:
                    l = lix(article)
                    p = percent_in_bag(article)
                    s = get_sentiment(article)
                    writer.writerow([article_id, label, l, p, s])
                except ZeroDivisionError:
                    print('Zero division at ' + article_id)
                    
if __name__ == '__main__':
    folders = [tokens_folder + folder for folder in os.listdir(tokens_folder)]
    folders = sorted(folders, key=lambda x: int(x.split('_')[-1].split('.')[0]))

    for folder in folders:
        process(folder)
