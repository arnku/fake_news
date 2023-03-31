import os
import csv
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

bago_folder = 'bagowords/'
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

csv.field_size_limit(1310720)

print("Loading data...")
# load bago
header = True
dataset_in = []
dataset_out = []
for bago_file in os.listdir(bago_folder):
    print(bago_file, end='\r')
    with open(bago_folder + bago_file, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        if header:
            header = next(reader)
        for row in reader:
            dataset_in.append((int(row[1]), int(row[2])))
            dataset_out.append(row[0])

print("Training model...")
# split dataset


dataset_out = [label_dict[row] for row in dataset_out]
X_train, X_test, y_train, y_test = train_test_split(dataset_in, dataset_out, test_size=0.2, random_state=42)

# train model
model = LogisticRegression()
model.fit(X_train, y_train)

print("Testing model...")
# test model
print("score: ", model.score(X_test, y_test))

import sklearn.metrics as metrics
import matplotlib.pyplot as plt
metrics.ConfusionMatrixDisplay.from_predictions(y_test, model.predict(X_test), normalize='all').plot()
print("precision_recall_fscore_support: ", metrics.precision_recall_fscore_support(y_test, model.predict(X_test), average='binary'))

print("always guess correct: ", sum(y_test)/len(y_test))
print("always guess incorrect: ", 1 - sum(y_test)/len(y_test))

# Save model
import pickle
with open('model_a.pkl', 'wb') as f:
    pickle.dump(model, f)