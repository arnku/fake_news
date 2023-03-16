import csv
import os
import math

def tf(article):
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

def df(tokens_list):
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

def get_number_of_articles(tokens_list):
    n = 0
    for articles in tokens_list:
        with open(articles, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            header = next(reader)
            n += sum([1 for row in reader])
    return n

def idf(df, n):
    idf = {}
    for word, count in df.items():
        idf[word] = math.log(n / float(count),2)
    return idf

def tf_idf(tf, idf):
    tf_idf = {}
    for word, t in tf.items():
        tf_idf[word] = t * idf[word]
    return tf_idf

test_file = 'tokens/token_split_0.csv'
test_df = df([test_file])
test_n = get_number_of_articles([test_file])
test_idf = idf(test_df, test_n)

with open(test_file, 'r') as f:
    reader = csv.reader(f)
    header = next(reader)
    tf_list = []
    for row in reader:
        tf_list.append((row[0],tf(row[1])))

tf_idf_list = []
for label, tf in tf_list:
    tf_idf_list.append((label, tf_idf(tf, test_idf))) 

# save tf-idf
with open('tf-idf_split_0.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'tf-idf'])
    for tf_idf in tf_idf_list:
        writer.writerow(tf_idf)