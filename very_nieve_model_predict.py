import os
import csv
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

bago_folder = 'bagowords/'
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

# import model
import pickle
model_path = 'nieve_model.pkl'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

print(model.score(dataset_in, dataset_out))

import sklearn.metrics as metrics
import matplotlib.pyplot as plt
metrics.ConfusionMatrixDisplay.from_predictions(dataset_out, model.predict(dataset_in)).plot()
plt.show()
print("precision_recall_fscore_support:", metrics.precision_recall_fscore_support(dataset_out, model.predict(dataset_in), average='micro'))