import csv
import os
import regex as re

file_name = 'BIG.csv'
save_file = 'removed_words.csv'

# Allow for larger lines
csv.field_size_limit(1310720)

# regex to remove non-latin characters
re_non_latin = re.compile(r'[^\p{Latin}|\s]')

removed_dict = {}
with open(file_name, 'r') as r:
    reader = csv.reader(r)
    header = next(reader) # skip header    
    for i, row in enumerate(reader):
        print(i, end='\r')
        try:
            removed = re_non_latin.findall(row[5])
            for word in removed:
                if word in removed_dict:
                    removed_dict[word] += 1
                else:
                    removed_dict[word] = 1
        except:
            continue

# save removed words to csv
with open(save_file, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(('word', 'count'))
    for word, count in removed_dict.items():
        writer.writerow((word, count))
