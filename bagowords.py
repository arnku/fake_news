import os
import csv

dfs_file = 'dfs.csv'
tokens_folder = 'tokens/'
output_folder = 'bagowords/'

os.makedirs(output_folder, exist_ok=True)

# load dfs
dfs = {}
with open(dfs_file, 'r') as f:
    reader = csv.reader(f, delimiter=',')
    header = next(reader)
    for i, row in enumerate(reader):
        dfs[row[0]] = i

dfs_len = len(dfs)

# load tokens
header = False
for token_file in os.listdir(tokens_folder):
    with open(tokens_folder + token_file, 'r') as f:
        with open(output_folder + "bago_" + token_file, 'w') as output_file:
            reader = csv.reader(f, delimiter=',')
            writer = csv.writer(output_file, delimiter=',')
            if header:
                header = next(reader)
            writer.writerow(('id', 'n_not_in_bag', 'len_of_bag', dfs))
            for row in reader:
                words = row[1].split()
                bag = []
                not_in_bag = 0
                for word in words:
                    if word in dfs:
                        bag.append(dfs[word])
                    else:
                        not_in_bag += 1
                writer.writerow((row[0], not_in_bag, len(bag), bag))
    print("Finished " + token_file)

                    
                