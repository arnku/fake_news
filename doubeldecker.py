import os
import csv
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import ast


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
dataset_in_bag = []
dataset_in_stats = []
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
            if int(row[2]) == 0:
                print("Zero length")
                continue
            l = [0] * dfs_len
            for v in ast.literal_eval(row[3]):
                if int(v) >= dfs_len:
                    continue
                l[int(v)] = 1
            dataset_in_bag.append(l)
            dataset_in_stats.append(int(row[1])/int(row[2]))
            dataset_out.append(label_dict[row[0]])

print("Splitting data...")
X_train_bag, X_test_bag, X_train_stat, X_test_stat, y_train, y_test = train_test_split(dataset_in_bag, dataset_in_stats, dataset_out, test_size=0.2, random_state=0)
X_train_bag_1, X_train_bag_2, X_train_stat_1, X_train_stat_2, y_train_1, y_train_2 = train_test_split(X_train_bag, X_train_stat, y_train, test_size=0.5, random_state=0)

print("Training...")
layer1 = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial', max_iter=1000)
layer2 = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial', max_iter=1000)

layer1.fit(X_train_bag_1, y_train_1)
p2 = layer1.predict(X_train_bag_2)
X_train2 = list(zip(p2, X_train_stat_2))
layer2.fit(X_train2, y_train_2)

print("Testing...")
p1 = layer1.predict(X_test_bag)
print(layer1.score(X_test_bag, y_test))
X_test2 = list(zip(p1, X_test_stat))
layer2.predict(X_test2)
print(layer2.score(X_test2, y_test))


