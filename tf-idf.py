import csv
import os
import math

tokens_folder = 'numerated/'
csv.field_size_limit(1310720)


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

def df(tokens_list : list, verbose = False) -> dict:
    '''
    How many articles each word is in.
    Takes a list of strings (token files) as input and returns a dictionary.
    '''
    df = {}
    for i, articles in enumerate(tokens_list):
        if verbose:
            print(i, end='\r')
        with open(articles, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            header = next(reader)
            for article in reader:
                words = article[2].split()
                # remove duplicates
                words = list(set(words))
                for word in words:
                    if word in df:
                        df[word] += 1
                    else:
                        df[word] = 1
    print('Done df')
    return df

def get_number_of_articles(tokens_list : list, verbose = False) -> int:
    '''
    Returns the number of articles in the dataset.
    Takes a list of strings (token files) as input and returns an integer.
    '''
    n = 0
    for articles in tokens_list:
        if verbose:
            print(n, end='\r')
        with open(articles, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            header = next(reader)
            n += sum([1 for row in reader])
    print(n)
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
    Takes a dictionary (tf) and a dictionary (idf) as input and returns a list of tuples.
    '''
    tf_idf = []
    for word, t in tf.items():
        tf_idf.append((word, t * idf[word]))
    return tf_idf

print('Loading files...')
token_files = os.listdir(tokens_folder)
token_files = [tokens_folder + file for file in token_files]

print('Calculating idf...')
dfs = df(token_files, verbose=True)
n_articles = get_number_of_articles(token_files, verbose=True)
idfs = idf(dfs, n_articles)

percent_word_cutoff = 0.01 / 100 # if a word is in less than 0.1% of the articles, remove it
absolute_word_cutoff = 10000
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
        if i >= absolute_word_cutoff:
            print("Max number of rows reached.")
            break
        #if i >= 1048576 - 1:
        #    print("Max number of rows reached.")
        #    break
        writer.writerow(df_)


from multiprocessing import Pool

save_folder = 'tf-idf/'
os.makedirs(save_folder, exist_ok=True)

def process_file(token_file):
    tf_list = []
    with open(token_file, 'r') as f:
        reader = csv.reader(f)
        #header = next(reader)
        for row in reader:
            tf_list.append((row[0], row[1],tf(row[2])))

    tfidf_list = []
    for i, label, tf_ in tf_list:
        try:
            a = tf_idf(tf_, idfs)
        except KeyError:
            print('KeyError: ' + i)
            continue
        if len(a) == 0:
            print('Empty list: ' + i)
            continue
        tfidf_list.append((i, label, a)) 


    # save tf-idf
    with open(save_folder + 'tf-idf_' + token_file.split('/')[-1], 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['i', 'id', 'tf-idf'])
        for tf_idf_ in tfidf_list:
            writer.writerow(tf_idf_)

    print('Done with ' + token_file)

if __name__ == '__main__':
    with Pool() as p:
        p.map(process_file, token_files)