'''
Randomizes the order of lines in a csv file.
Saves the randomized files in a new folder with the same number of files as the original folder.
'''
import os
import csv
import random

input_folder = 'splits/'
save_folder = 'splits_randomized/' 

os.makedirs(save_folder, exist_ok=True)
csv.field_size_limit(1310720)

num_tokens = 0
csv_list = []
for tokens in os.listdir(input_folder):
    num_tokens += 1
    csv_list.append(csv.writer(open(save_folder + "rand_" + tokens, 'w')))

print("Number of tokens: " + str(num_tokens))

for i,tokens in enumerate(os.listdir(input_folder)):
    print(i, end='\r')
    tokensPath = input_folder + tokens

    with open(tokensPath, 'r') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)

        for row in reader:
            rando = random.randint(0, num_tokens - 1)
            csv_list[rando].writerow(row)