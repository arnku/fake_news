import os
import csv
from sklearn.neural_network import MLPClassifier
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split
import ast
import numpy as np
import scipy.sparse as sp


sparce_matrix_folder = 'testrrr2/'
features_folder = 'test1/'
dfs_file = 'dfs.csv'
n_fetures = 4

csv.field_size_limit(1310720)

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
    'political': True
    }

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

# sort files
sm_folders = sorted(os.listdir(sparce_matrix_folder), key=lambda x: int(x.split('_')[-1].split('.')[0])) 
fe_folders = sorted(os.listdir(features_folder), key=lambda x: int(x.split('_')[-1].split('.')[0]))

for i, (matrix_file, feature_file) in enumerate(zip(sm_folders, fe_folders)):

    with open(sparce_matrix_folder + matrix_file, 'r') as sm:
        with open(features_folder + feature_file, 'r') as fe:
            sm_reader = csv.reader(sm, delimiter=',')
            fe_reader = csv.reader(fe, delimiter=',')

            if header:
                next(sm_reader)
                next(fe_reader)

            rows = []
            cols = []
            vals = []
            n_row = 0

            for sm in sm_reader:

                article_id, word_id = sm[1], sm[2]
                article_id = int(article_id)

                if article_id not in labels:
                    labels[article_id] = (label_dict[sm[0]])

                if article_id != last_row:

                    # add fetures
                    fetures = next(fe_reader)
                    article_id_fe = fetures[0]
                    fetures = fetures[2:]
                    if article_id - 1 != int(article_id_fe):
                        print(article_id, article_id_fe)
                        raise Exception("Wrong order")
                    
                    for j, feature in enumerate(fetures):
                        rows.append(n_row)
                        cols.append(dfs_len + 1 + j)
                        vals.append(float(feature))

                    last_row = article_id
                    n_row += 1

                rows.append(n_row)
                cols.append(int(word_id))
                vals.append(float(sm[3]))

            if first_time:
                first_time = False
                sparce_matrix = csr_matrix((vals, (rows, cols)), shape=(n_row + 1, dfs_len + n_fetures + 1))

            else:
                sparce_matrix = sp.vstack([sparce_matrix, csr_matrix((vals, (rows, cols)), shape=(n_row + 1, dfs_len + n_fetures + 1))])

            last_row += 1


# sort labels
labels_n = []
for i in range(len(labels)):
    labels_n.append(labels[i])
del labels

print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(sparce_matrix, labels_n, test_size=0.2, random_state=42)
del sparce_matrix
del labels_n

print("Training...")
clf = MLPClassifier().fit(X_train, y_train)

print("Testing...")
print(clf.score(X_test, y_test))

# save model
import pickle
with open('mlp_model.pkl', 'wb') as f:
    pickle.dump(clf, f)

import matplotlib.pyplot as plt
import sklearn.metrics as metrics
metrics.ConfusionMatrixDisplay.from_predictions(y_test, clf.predict(X_test), normalize='all').plot()
plt.show()
print("precision_recall_fscore_support:", metrics.precision_recall_fscore_support(y_test, clf.predict(X_test), average='binary'))