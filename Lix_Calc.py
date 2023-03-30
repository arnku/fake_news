import os
import csv
import statistics


token_dirs = 'tokens/token_rand_split_220000.csv'
list = []

with open(token_dirs,'r') as input_file: 
    reader = csv.reader(input_file)
    for row in reader:
        list.append(row)

def calc_lix(dict_ : dict) -> dict:
    lix_dict = {}
    for label, words in dict_.items():
        total_words = 0.0
        total_long_words = 0.0
        total_lix_list = []
        for i in words[1:]:
            total_long_words = 0.0
            total_words = len(i.split())
            if total_words == 0:
                total_lix_list.append(0)
                continue
            for j in i.split():
                if len(j) >= 7:
                    total_long_words += 1
            total_lix_list.append((total_long_words*100)/total_words)
        lix_dict[label] = total_lix_list
    return lix_dict

def sort_list_by_label(list : list) -> dict:
    label_dict = {}
    for label, words in list[1:]:
        if label not in label_dict:
            label_dict[label] = [[words]]
        label_dict[label].append(words)
    return label_dict

def mean_lix(list):
    return sum(list)/len(list)

def median_lix(list):
    return statistics.median(list)
    
def std_lix(l1,l2):
    return (sum((i - l1)**2 for i in l2)/len(l2))**0.5

label_dict = sort_list_by_label(list)
label_lix = calc_lix(label_dict)


for label, lix in label_lix.items():
    print(label)
    #print("reliable:", calc_lix(lix))
    print("Mean lix numbers:")
    reliable_mean_lix = mean_lix(lix)
    print(reliable_mean_lix)
    print("Median lix numbers:")
    reliable_median_lix = median_lix(lix)
    print(reliable_median_lix)
    print("STANDARD DEVIATION lix numbers:")
    reliable_std_lix = std_lix(reliable_mean_lix, lix)
    print( reliable_std_lix)
    print("____________________________________________________")

        

#plot label_lix
import matplotlib.pyplot as plt
import numpy as np

<<<<<<< HEAD

""" for label, lix in label_lix.items():
    print(label)
    plt.hist(lix, bins=20)
    plt.title(label)
    plt.show()
=======
#for label, lix in label_lix.items():
#    plt.hist(lix, bins=20)
#    plt.title(label)
#    plt.show()
>>>>>>> 1a78db82b8d7916e65e8d5724bf28d22a5fc9def

# plot all in one

for label, lix in label_lix.items():
    plt.hist(lix, bins=20)
plt.title("All")
plt.show() """


#plot label_lix with mean and median

D = [label_lix['reliable'], 
     label_lix['unreliable'],
     label_lix['fake'],
     label_lix['satire'],
     label_lix['conspiracy'],
     label_lix['bias'],
     label_lix['junksci'],
     label_lix['hate'],
     label_lix['political'],
     label_lix['clickbait'],
     label_lix['rumor']]

plt.boxplot(D, 
            notch=None, 
            sym=None, 
            vert=None, 
            whis=None, 
            positions=None, 
            widths=None, 
            patch_artist=None, 
            bootstrap=None, 
            usermedians=None, 
            conf_intervals=None, 
            meanline=None, 
            showmeans=None, 
            showcaps=None, 
            showbox=None, 
            showfliers=False, 
            boxprops=None, 
            labels=['reliable','unreliable','fake','satire','conspiracy','bias','junksci','hate','political','clickbait','rumor'], 
            flierprops=None, 
            medianprops=None, 
            meanprops=None, 
            capprops=None, 
            whiskerprops=None, 
            manage_ticks=True, 
            autorange=False, 
            zorder=None, 
            capwidths=None,
            data=None)
plt.show()



