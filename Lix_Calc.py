import os
import csv


token_dirs = 'tokens_randomized/rand_token_split_0.csv'
list = []

with open(token_dirs,'r') as input_file: 
    reader = csv.reader(input_file)
    for row in reader:
        list.append(row)

def calc_lix(list):
    total_words = 0
    total_long_words = 0
    for i in list[1:]:
        total_words = len(i.split())
        for j in i.split():
            if len(j) > 6:
                total_long_words += 1
    return (total_long_words*100)/total_words

def sort_list_by_label(list):
    reliable_list = []
    unreliable_list = []
    for i in list[1:]:
        if i[0] == 'reliable':
            reliable_list.append(i[1])
        else:
            unreliable_list.append(i[1])
    return reliable_list, unreliable_list

def mean_lix(list):
    total_lix = 0
    for i in list:
        total_lix += calc_lix(i)
    return total_lix/len(list)

reliable_list, unreliable_list = sort_list_by_label(list)

print("reliable:", calc_lix(reliable_list))

reliable_mean_lix = mean_lix(reliable_list)
unreliable_mean_lix = mean_lix(unreliable_list)

print("reliable:", reliable_mean_lix)
print("unreliable:", unreliable_mean_lix)

       
