import os
import csv
from time import time
from multiprocessing import Pool

save_path = 'stats_r/'
tokens_folder = 'tokens_randomized/'

os.makedirs(save_path, exist_ok=True)

def process_file(token_path):
    start_time = time()
    with open(tokens_folder + token_path, 'r') as input_file:
        reader = csv.reader(input_file)    
        header = next(reader) # skip header

        haderDict = {}
        for row in reader:
            if not row[0] in haderDict:
                haderDict[row[0]] = {}
            for word in row[1].split():
                if not word in haderDict[row[0]]:
                    haderDict[row[0]][word] = 1
                haderDict[row[0]][word] += 1
    
    with open(save_path + "stats_" + token_path, 'w') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['label', 'word', 'count'])
        for label in haderDict:
            for word in haderDict[label]:
                writer.writerow([label, word, haderDict[label][word]])
    
    print(f"Processed {token_path} in {round((time() - start_time)/60,3)} minutes.")
    

if __name__ == '__main__':
    with Pool() as p:
        p.map(process_file, os.listdir(tokens_folder))
