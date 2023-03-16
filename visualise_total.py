import matplotlib.pyplot as plt
import csv

stat_file = 'word_stats_total.csv'

stat_dict = {}
with open(stat_file, 'r') as input_file:
    reader = csv.reader(input_file)
    header = next(reader) # skip header
    
    for row in csv.reader(input_file):
        if not row[0] in stat_dict:
            stat_dict[row[0]] = {}
        if not row[1] in stat_dict[row[0]]:
            stat_dict[row[0]][row[1]] = int(row[2])
        else:
            stat_dict[row[0]][row[1]] += int(row[2])

# Sort the words by their count
for label in stat_dict:
    stat_dict[label] = {k: v for k, v in sorted(stat_dict[label].items(), key=lambda item: item[1], reverse=True)}

def label_count():
    print("labels:")
    for label in stat_dict:
        print(label, f"{len(stat_dict[label]):,}")

def save_word_count_per_label():
    for label in stat_dict:
        with open('word_count_' + label + '.csv', 'w') as output_file:
            writer = csv.writer(output_file, delimiter=';')
            writer.writerow(['label', 'word', 'count'])
            for word in stat_dict[label]:
                writer.writerow([label, word, stat_dict[label][word]])

def combine_dicts(stat_dict):
    # combine all labels into one dict
    total_dict = {}
    for label in stat_dict:
        for word in stat_dict[label]:
            if not word in total_dict:
                total_dict[word] = stat_dict[label][word]
            else:
                total_dict[word] += stat_dict[label][word]
    total_dict = {k: v for k, v in sorted(total_dict.items(), key=lambda item: item[1], reverse=True)}
    return total_dict

def save_word_count_total():
    total_dict = combine_dicts(stat_dict)
    # save to file
    with open('word_count_total.csv', 'w') as output_file:
        writer = csv.writer(output_file, delimiter=';')
        writer.writerow(['label', 'word', 'count'])
        for word in total_dict:
            writer.writerow(['total', word, total_dict[word]])

def get_total_words_count(dict_to_count):
    total_dict = combine_dicts(dict_to_count)
    total_words = 0
    for word in total_dict:
        total_words += total_dict[word]
    return total_words

def cut_off_words(percent):
    total_dict = combine_dicts(stat_dict)
    # cut off words that are less than the percent
    total_words = get_total_words_count(stat_dict)
    cutoff = total_words * percent
    total_dict = {k: v for k, v in total_dict.items() if v > cutoff}

    with open('word_count_cutoff.csv', 'w') as output_file:
        writer = csv.writer(output_file, delimiter=';')
        writer.writerow(['word', 'count'])
        for word in total_dict:
            writer.writerow([word, total_dict[word]])

    return total_dict
