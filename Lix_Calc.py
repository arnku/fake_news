import os
import csv


token_dirs = 'tokens_randomized/'
list = []

with open(token_dirs,'r') as input_file: 
    reader = csv.reader(input_file)
    for row in reader:
        list.append(row)

def calc_lix(list):
    total_words = 0.0
    total_long_words = 0.0
    total_lix_list = []
    for i in list[1:]:
        total_long_words = 0.0
        total_words = len(i.split())
        for j in i.split():
            if len(j) > 6:
                total_long_words += 1
        total_lix_list.append((total_long_words*100)/total_words)
    return total_lix_list

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
    return sum(list)/len(list)
    
def std_lix(l1,l2):
    return (sum((i - l1)**2 for i in l2)/len(l2))**0.5

reliable_list, unreliable_list = sort_list_by_label(list)
reliable_lix = calc_lix(reliable_list)
unreliable_lix = calc_lix(unreliable_list)

""" print("reliable:", calc_lix(reliable_list)) """

print("_______________________________________________________________________________________________")
print("")
print("")
print("MEAN lix numbers:")
reliable_mean_lix = mean_lix(reliable_lix)
unreliable_mean_lix = mean_lix(unreliable_lix)
print("reliable:", reliable_mean_lix)
print("unreliable:", unreliable_mean_lix)
print("____________________________________________________")
print("")
print("")
print("STANDARD DEVIATION lix numbers:")
reliable_std_lix = std_lix(reliable_mean_lix, reliable_lix)
unreliable_std_lix = std_lix(unreliable_mean_lix, unreliable_lix)
print("reliable:", reliable_std_lix)
print("unreliable:", unreliable_std_lix)
print("____________________________________________________")
print("")
print("")

       
