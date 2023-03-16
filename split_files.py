import csv
import os
import regex as re

save_path = 'splits/'
file_name = 'BIG.csv'
split_size = 20000 # Number of lines per file

# Create folder to save the splits
os.makedirs(save_path, exist_ok=True)

# Allow for larger lines
csv.field_size_limit(1310720)

# regex to remove punctuation
re_punctuation = re.compile(r'[\p{P}\p{S}\r\n]')
# regex to remove non-latin characters
re_non_latin = re.compile(r'[^\p{Latin}]')

error_count = 0
with open(file_name, 'r') as r:
    reader = csv.reader(r)
    header = next(reader) # skip header
    
    for i, row in enumerate(reader):
        # Create a new file every 20000 lines
        if i % split_size == 0:
            if i != 0:
                f.close()
            f = open(save_path + 'split_' + str(i) + '.csv', 'w')
            print(f"{i:,} lines processed with {error_count} total errors")
            writer = csv.writer(f)
            writer.writerow(('header', 'content'))
        
        # Remove punctuation and non-latin characters
        try:
            content = re_punctuation.sub(' ', row[5])
            content = re_non_latin.sub('', content)
            if content.isspace():
                continue
            writer.writerow((row[3], content))
        except:
            error_count += 1
            continue