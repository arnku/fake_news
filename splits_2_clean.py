'''
This script takes the splits folder and cleans the text in the content column.
It then saves the cleaned text in the tokens folder.

Should be run after split_files.py

Does not take a lot of ram, but does use all cpu cores.
'''

import os
import cleantext
from multiprocessing import Pool
from time import time
import csv

'''
Fake:
- Bias
- Satire
- Rumor
- Conspiracy
- Hate
- Fake
- Junksci
- Unreliable
- Clickbait

Reliable:
- Reliable
- Political
'''
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

splits_folder = 'splits_randomized/'
save_path = 'tokens/'

csv.field_size_limit(1310720)
os.makedirs(save_path, exist_ok=True)

def process_file(split_path):
    header = False

    start_time = time()
    error_count = 0
    with open(splits_folder + split_path, 'r') as input_file:
        with open(save_path + "token_" + split_path, 'w') as output_file:
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)

            if header:
                header = next(reader) # skip header
                writer.writerow(header)

            for row in reader:
                if not row[0] in label_dict:
                    continue
                row[0] = label_dict[row[0].lower()]
                
                content = cleantext.clean_words(row[1], clean_all= True)
                writer.writerow((row[0],' '.join(content)))

    os.remove(splits_folder + split_path)
    print(f"Processed {split_path} in {round((time() - start_time)/60,3)} minutes with {error_count} errors.")

if __name__ == '__main__':
    with Pool() as p:
        p.map(process_file, os.listdir(splits_folder))
