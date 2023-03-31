import os
import csv
from sklearn.linear_model import LogisticRegression
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split
import ast
import numpy as np
import scipy.sparse as sp


sparce_matrix_folder = 'reduced_matrix/'
dfs_file = 'dfs.csv'
label_dict = {
    'bias': False,
    'satire': False,
    'rumor': False,
    'conspiracy': False,
    'hate': False,
    'fake': False,
    'junksci': False,
    'unreliable': False,
    'clickbait': False,
    'reliable': True,
    'political': True,

    'pants-fire': False,
    'false': False,
    'half-true': False,
    'barely-true': False,
    'mostly-true': False,
    'true': True,
    }

csv.field_size_limit(1310720)


# load dfs
dfs = {}
with open(dfs_file, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    header = next(reader)
    for i, r in enumerate(reader):
        dfs[r[0]] = i
dfs_len = len(dfs)

print("Loading data...")
header = True

labels = {}
first_time = True
last_row = 0

sm_files = sorted(os.listdir(sparce_matrix_folder), key=lambda x: int(x.split('_')[-1].split('.')[0]))

for i, matrix_file in enumerate(sm_files):
    if i > 25:
        break
    print(matrix_file)
    with open(sparce_matrix_folder + matrix_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        if header:
            header = next(reader)

        rows = []
        cols = []
        vals = []
        n_row = 0

        for row in reader:

            article_id, word_id = row[1], row[2]
            article_id = int(article_id)

            if article_id not in labels:
                labels[article_id] = (label_dict[row[0]])

            if article_id != last_row:
                last_row = article_id
                n_row += 1

            rows.append(n_row)
            cols.append(int(word_id))
            vals.append(1)

        if first_time:
            first_time = False
            sparce_matrix = csr_matrix((vals, (rows, cols)), shape=(n_row + 1, dfs_len))

        else:
            sparce_matrix = sp.vstack([sparce_matrix, csr_matrix((vals, (rows, cols)), shape=(n_row + 1, dfs_len))])

        last_row += 1


# sort labels
labels_n = []
for i in range(len(labels)):
    labels_n.append(labels[i])
del labels


# import model
import pickle
model_path = 'model_b.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

print(model.score(sparce_matrix, labels_n))

import matplotlib.pyplot as plt
import sklearn.metrics as metrics
metrics.ConfusionMatrixDisplay.from_predictions(labels_n, model.predict(sparce_matrix), normalize='all').plot()
plt.show()
print("precision_recall_fscore_support:", metrics.precision_recall_fscore_support(labels_n, model.predict(sparce_matrix), average='binary'))  
