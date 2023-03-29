import os
import csv
from multiprocessing import Pool
import ast


words_file = 'dfs.csv'
tf_idf_folder = 'tf-idf/'
save_folder = 'reduced_matrix/'

os.makedirs(save_folder, exist_ok=True)
csv.field_size_limit(1310720)

word_id_dict = {}
header = True
with open(words_file, 'r') as f:
    reader = csv.reader(f)
    if header:
        next(reader)
    for row in reader:
        word_id_dict[row[0]] = len(word_id_dict)

def process_file(tf_idf):
    n = int(tf_idf.split('_')[-1].split('.')[0])
    with open(tf_idf, 'r') as f:
        with open(save_folder + 'rematrix_' + tf_idf.split('/')[-1], 'w') as g:
            reader = csv.reader(f)
            writer = csv.writer(g)
            next(reader)
            writer.writerow(['label', 'acc_not_in_bag', 'articel_id', 'word_id', 'tf_idf)'])
            for i, row in enumerate(reader):
                label = row[0]
                tf_idf_ = ast.literal_eval(row[1])
                if len(tf_idf_) == 0:
                    continue
                not_in_bag = 0
                for (word, val) in tf_idf_:
                    if word not in word_id_dict:
                        not_in_bag += 1
                        continue
                    writer.writerow([label,not_in_bag, n + i, word_id_dict[word], val])
                not_in_bag = not_in_bag / len(tf_idf_)
    print('Processed ' + tf_idf)

def remove_gaps(files):
    '''
    Goes through all files and removes gaps in the article ids
    '''
    # sort files
    files = sorted(files, key=lambda x: int(x.split('_')[-1].split('.')[0]))
    os.makedirs("tmp", exist_ok=True)
    n = 0
    last_n = 0
    for file_ in files:
        print(file_)
        with open(save_folder + file_, 'r') as f:
            with open("tmp/" + file_, 'w') as g:
                reader = csv.reader(f)
                writer = csv.writer(g)
                header = next(reader)
                writer.writerow(header)
                for row in reader:
                    id_ = int(row[2])
                    if id_ > last_n:
                        n += 1
                        last_n = id_
                    row[2] = n
                    writer.writerow(row)   
                    
    # remove old files
    for file_ in files:
        os.remove(save_folder + file_)
    # move new files
    for file_ in os.listdir("tmp"):
        os.rename("tmp/" + file_, save_folder + file_)
    os.rmdir("tmp")

          
if __name__ == '__main__':
    #tf_idf_files = [tf_idf_folder + file for file in os.listdir(tf_idf_folder)]
    #with Pool() as p:
    #    p.map(process_file, tf_idf_files)
    remove_gaps(os.listdir(save_folder))