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
    with open(tf_idf, 'r') as f:
        with open(save_folder + 'rematrix_' + tf_idf.split('/')[-1], 'w') as g:
            reader = csv.reader(f)
            writer = csv.writer(g)
            next(reader)
            writer.writerow(['label', 'articel_id', 'word_id', 'tf_idf)'])
            for row in enumerate(reader):
                i = int(row[0])
                label = row[1]
                tf_idf_ = ast.literal_eval(row[2])
                for (word, val) in tf_idf_:
                    if word not in word_id_dict:
                        continue
                    writer.writerow([label, i, word_id_dict[word], val])
    print('Processed ' + tf_idf)

if __name__ == '__main__':
    tf_idf_files = [tf_idf_folder + file for file in os.listdir(tf_idf_folder)]
    with Pool() as p:
        p.map(process_file, tf_idf_files)
