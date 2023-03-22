import csv
import os
import regex as re

file_name = 'BIG.csv'

csv.field_size_limit(1310720)

label_dict = {
    'bias': 'fake', 
    'satire': 'fake',
    'rumor': 'fake',
    'conspiracy': 'fake',
    'hate': 'fake',
    'fake': 'fake',
    'junksci': 'fake',
    'unreliable': 'fake',
    'clickbait': 'fake',
    'reliable': 'reliable',
    'political': 'reliable'
    }

print("Loading data...")

authors_data = []
website_data = []
out_data = []

with open(file_name, 'r') as r:
    reader = csv.reader(r)
    header = next(reader) # skip header
    print(header)
    for i, row in enumerate(reader):
        if i % 10000 == 0:
            print(i, end='\r')
        if len(row) < 11:
            continue
        if row[3] not in label_dict:
            continue
        out_data.append(label_dict[row[3]])
        authors_data.append(row[10])
        website_data.append(row[2])


# Give each author a unique id
author_dict = {}
for author in authors_data:
    if author not in author_dict:
        author_dict[author] = len(author_dict)
authors_data = [author_dict[author] for author in authors_data]

# Give each website a unique id
website_dict = {}
for website in website_data:
    if website not in website_dict:
        website_dict[website] = len(website_dict)
website_data = [website_dict[website] for website in website_data]
data = [[a, w] for a, w in zip(authors_data, website_data)]

# Turn labels into true or false
out_data = [False if o == 'fake' else True for o in out_data]

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# split dataset
X_train, X_test, y_train, y_test = train_test_split(data, out_data, test_size=0.2)

# train model
model = LogisticRegression()
model.fit(X_train, y_train)

print("Testing model...")
# test model
print("score: ", model.score(X_test, y_test))
print("always guess correct: ", sum(y_test)/len(y_test))
print("always guess incorrect: ", 1 - sum(y_test)/len(y_test))