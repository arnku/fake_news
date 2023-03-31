'''
Splits a large csv file into smaller files of a specified size.
Also removes punctuation and non-latin characters.
'''

import csv
import os
import regex as re

file_name = 'FakeNewsCorpus.csv'
save_path = 'splits/'
split_size = 20000 # Number of lines per file

# Create folder to save the splits
os.makedirs(save_path, exist_ok=True)

# Allow for larger lines
csv.field_size_limit(1310720)

# regex to remove non-latin characters
re_non_latin = re.compile(r'[^\p{Latin}|\s|:\/._\-?=|0-9]')
re_only_letters = re.compile(r'[^\p{Latin}]')

error_count = 0
invalid_count = 0
total_valid_count = 0
with open(file_name, 'r') as r:
    reader = csv.reader(r)
    header = next(reader) # skip header
    
    for i, row in enumerate(reader):
        # Create a new file every 20000 lines
        if i % split_size == 0:
            if i != 0:
                f.close()
            f = open(save_path + 'split_' + str(i) + '.csv', 'w')
            print(f"{i:,} lines processed with {error_count} total errors and {invalid_count} invalid.")
            writer = csv.writer(f)
            writer.writerow(('header', 'content'))
        
        # Remove punctuation and non-latin characters
        try:
            content = re_non_latin.sub(' ', row[5])
            if re_only_letters.sub(' ', content).isspace() or not content: # Remove articles with only non-latin characters
                invalid_count += 1
                continue
            writer.writerow((row[3], content))
            total_valid_count += 1
        except:
            error_count += 1
            continue
print(f"{i:,} lines processed with {error_count} total errors and {invalid_count} invalid. {total_valid_count:,} valid lines.")
# 8,529,193 lines processed with 238 total errors and 42364 invalid. 8,486,592 valid lines.