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
            writer.writerow(['id', 'percent_not_in_bag', 'reduced_matrix'])
            for row in reader:
                label = row[0]
                tf_idf_ = ast.literal_eval(row[1])
                if len(tf_idf_) == 0:
                    continue
                not_in_bag = 0
                rm = []
                for (word, val) in tf_idf_:
                    if word not in word_id_dict:
                        not_in_bag += 1
                        continue
                    rm.append((word_id_dict[word], val))
                not_in_bag = not_in_bag / len(tf_idf_)
                writer.writerow([label, not_in_bag, rm])
    print('Processed ' + tf_idf)
            
if __name__ == '__main__':
    tf_idf_files = [tf_idf_folder + file for file in os.listdir(tf_idf_folder)]
    with Pool() as p:
        p.map(process_file, tf_idf_files)