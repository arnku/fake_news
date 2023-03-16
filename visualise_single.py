'''
Data visualisation for single stat file
'''

import csv
import os

stats_folder = 'stats_r/'
header = True


print("Reading stats files...")
stats_list = []
for i, stats in enumerate(os.listdir(stats_folder)):
    print(i, end='\r')
    stat_dict = {}
    with open(stats_folder + stats, 'r') as input_file:
        reader = csv.reader(input_file)
        if header:
            header = next(reader) # skip header
        for row in reader:
            if not row[0] in stat_dict:
                stat_dict[row[0]] = {}
            if not row[1] in stat_dict[row[0]]:
                stat_dict[row[0]][row[1]] = int(row[2])
            else:
                stat_dict[row[0]][row[1]] += int(row[2])
    for label in stat_dict:
        stat_dict[label] = {k: v for k, v in sorted(stat_dict[label].items(), key=lambda item: item[1], reverse=True)}
    stats_list.append(stat_dict)
print("Done reading stats files.")

def show_file_label_distrobution():
    for i,stats in enumerate(stats_list):
        print(i, end=' ')
        for label in stats:
            print(f"{len(stats[label]):,}", end = ' ')
        print()
