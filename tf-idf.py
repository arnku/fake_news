import csv
import os
import math

def tf(article : str) -> dict:
    '''
    How many procent each word is in the article.
    Takes a string (one article) as input and returns a dictionary.
    '''
    tf = {}
    word_count = 0
    for word in article.split():
        word_count += 1
        if word in tf:
            tf[word] += 1
        else:
            tf[word] = 1
    
    for word, count in tf.items():
        tf[word] = count / float(word_count)
    
    return tf

def df(tokens_list : list) -> dict:
    '''
    How many articles each word is in.
    Takes a list of strings (token files) as input and returns a dictionary.
    '''
    df = {}
    for articles in tokens_list:
        with open(articles, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            header = next(reader)
            for article in reader:
                words = article[1].split()
                # remove duplicates
                words = list(set(words))
                for word in words:
                    if word in df:
                        df[word] += 1
                    else:
                        df[word] = 1
    return df

def get_number_of_articles(tokens_list : list) -> int:
    '''
    Returns the number of articles in the dataset.
    Takes a list of strings (token files) as input and returns an integer.
    '''
    n = 0
    for articles in tokens_list:
        with open(articles, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            header = next(reader)
            n += sum([1 for row in reader])
    return n

def idf(df, n):
    '''
    Inverse document frequency. 
    Takes a dictionary (df) and an integer (n) as input and returns a dictionary.
    '''
    idf = {}
    for word, count in df.items():
        idf[word] = math.log(n / float(count),2)
    return idf

def tf_idf(tf, idf):
    '''
    Takes a dictionary (tf) and a dictionary (idf) as input and returns a dictionary.
    '''
    tf_idf = {}
    for word, t in tf.items():
        tf_idf[word] = t * idf[word]
    return tf_idf

print('Loading files...')
token_files = os.listdir('tokens')
token_files = ['tokens/' + file for file in token_files]

print('Calculating idf...')
dfs = df(token_files)
n_articles = get_number_of_articles(token_files)
idfs = idf(dfs, n_articles)

percent_word_cutoff = 0.01 / 100 # if a word is in less than 0.1% of the articles, remove it
cutoff_point = int(percent_word_cutoff * n_articles)

print('Total number of articles: ' + str(n_articles))
print('Cutoff point: ' + str(cutoff_point))

print('Sorting dfs...')
# sort dfs
dfs = sorted(dfs.items(), key=lambda x: x[1], reverse=True)
# save idfs
with open('dfs.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['word', 'idf'])
    for i, df_ in enumerate(dfs):
        if df_[1] < cutoff_point:
            print("Cutoff point reached.")
            break
        if i >= 1048576 - 1:
            print("Max number of rows reached.")
            break
        writer.writerow(df_)

'''

for token_file in token_files:
    print('Loading file: ' + token_file)
    print('Calculating tf...')
    tf_list = []
    with open(token_file, 'r') as f:
        reader = csv.reader(f)
        #header = next(reader)
        for row in reader:
            tf_list.append((row[0],tf(row[1])))


    print('Calculating tf-idf...')
    tfidf_list = []
    for label, tf_ in tf_list:
        tfidf_list.append((label, tf_idf(tf_, idfs))) 

    print('Saving tf-idf...')
    # save tf-idf
    with open('tf-idf_' + token_file.split('/')[-1], 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'tf-idf'])
        for tf_idf_ in tfidf_list:
            writer.writerow(tf_idf_)

'''