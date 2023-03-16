import os
import csv
import random

token_folder = 'tokens/'
save_folder = 'tokens_randomized/'

os.makedirs(save_folder, exist_ok=True)

num_tokens = 0
csv_list = []
for tokens in os.listdir(token_folder):
    num_tokens += 1
    csv_list.append(csv.writer(open(save_folder + "rand_" + tokens, 'w')))

print("Number of tokens: " + str(num_tokens))

for i,tokens in enumerate(os.listdir(token_folder)):
    print(i, end='\r')
    tokensPath = token_folder + tokens

    with open(tokensPath, 'r') as input_file:
        reader = csv.reader(input_file)
        header = next(reader)

        for row in reader:
            rando = random.randint(0, num_tokens - 1)
            csv_list[rando].writerow(row)

# close all files
for i in range(num_tokens):
    csv_list[i].close()