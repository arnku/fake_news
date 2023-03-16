import os
import cleantext
from multiprocessing import Pool
from time import time
import csv

splits_folder = 'splits/'
save_path = 'tokens/'
csv.field_size_limit(1310720)

os.makedirs(save_path, exist_ok=True)

def process_file(split_path):
    start_time = time()
    error_count = 0
    with open(splits_folder + split_path, 'r') as input_file:
        with open(save_path + "token_" + split_path, 'w') as output_file:
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)

            header = next(reader) # skip header
            writer.writerow(header)

            for row in reader:
                content = cleantext.clean_words(row[1], clean_all= True)
                writer.writerow((row[0],' '.join(content)))

    os.remove(splits_folder + split_path)
    print(f"Processed {split_path} in {round((time() - start_time)/60,3)} minutes with {error_count} errors.")

if __name__ == '__main__':
    with Pool() as p:
        p.map(process_file, os.listdir(splits_folder))
