import os
import csv
#from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
#from sklearn import naive_bayes
from scipy.sparse import csr_matrix
from sklearn.model_selection import train_test_split
import ast
import numpy as np


sparce_matrix_folder = 'reduced_matrix/'
dfs_file = 'dfs.csv'

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
    for i, row in enumerate(reader):
        dfs[row[0]] = i

dfs_len = len(dfs)

print("Loading data...")
# load bago
header = True

rows = []
cols = []
vals = []
labels = {}
for i, matrix_file in enumerate(os.listdir(sparce_matrix_folder)):
#for i, matrix_file in enumerate(["rematrix_tf-idf_fifty_token_rand_split_0.csv"]):
    print(matrix_file)
    with open(sparce_matrix_folder + matrix_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        if header:
            header = next(reader)
        for row in reader:
            article_id, word_id = row[2], row[3]
            article_id = int(article_id)
            if article_id not in labels:
                labels[article_id] = (label_dict[row[0]])
            
            rows.append(int(article_id))
            cols.append(int(word_id))
            vals.append(float(row[4]))



sparce_matrix = csr_matrix((vals, (rows, cols)))
del rows
del cols
del vals
# sort labels

labels_n = []
for i in range(len(labels)):
    try:
        labels_n.append(labels[i])
    except:
        pass
del labels

print(sparce_matrix.shape)
print(len(labels_n))


print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(sparce_matrix, labels_n, test_size=0.2, random_state=42)
del sparce_matrix
del labels_n

print("Training...")
clf = MLPClassifier(max_iter=100).fit(X_train, y_train)

print("Testing...")
print(clf.score(X_test, y_test))