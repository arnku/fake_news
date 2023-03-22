import os
import csv
import ast
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split



bago_folder = 'bagowords/'
dfs_file = 'dfs_reduced.csv'

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
dataset_in = []
dataset_out = []
for i, bago_file in enumerate(os.listdir(bago_folder)):
    if i > 1:
        break
    print(bago_file)
    with open(bago_folder + bago_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        if header:
            header = next(reader)
        for row in reader:
            l = [0] * dfs_len
            for v in ast.literal_eval(row[3]):
                if int(v) >= dfs_len:
                    continue
                l[int(v)] = 1
            dataset_in.append(l)
            dataset_out.append(label_dict[row[0]])

print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(dataset_in, dataset_out, test_size=0.2, random_state=42)
del dataset_in
del dataset_out

print("Training...")
clf = MultinomialNB()

clf.fit(X_train, y_train)

print("Testing...")
print(clf.score(X_test, y_test))