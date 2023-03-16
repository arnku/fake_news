import os
import csv

stats_folder = 'stats/'
save_file = 'word_stats_total.csv'

stat_dict = {}
for i,stat in enumerate(os.listdir(stats_folder)):
    print(i, end='\r')
    stat_path = stats_folder + stat

    with open(stat_path, 'r') as input_file:
        reader = csv.reader(input_file)
        header = next(reader) # skip header
        
        for row in csv.reader(input_file):
            if not row[0] in stat_dict:
                stat_dict[row[0]] = {}
            if not row[1] in stat_dict[row[0]]:
                stat_dict[row[0]][row[1]] = int(row[2])
            else:
                stat_dict[row[0]][row[1]] += int(row[2])
    
with open(save_file, 'w') as output_file:
    writer = csv.writer(output_file)
    writer.writerow(['label', 'word', 'count'])
    for label in stat_dict:
        for word in stat_dict[label]:
            writer.writerow([label, word, stat_dict[label][word]])