import os
import csv

tokens_folder = 'tokens/'
save_path = '50-50_split/'
label_dict = {
    'bias': 'unreliable',
    'satire': 'unreliable',
    'rumor': 'unreliable',
    'conspiracy': 'unreliable',
    'hate': 'unreliable',
    'fake': 'unreliable',
    'junksci': 'unreliable',
    'unreliable': 'unreliable',
    'clickbait': 'unreliable',
    'reliable': 'reliable',
    'political': 'reliable',
    }

os.makedirs(save_path, exist_ok=True)
csv.field_size_limit(1310720)


def count_label(files, folder = tokens_folder):
    '''
    Count the number of articles for each label
    '''
    label_count = {}
    for file_ in files:
        with open(folder + file_, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                label = label_dict[row[0]]
                if label not in label_count:
                    label_count[label] = 1
                else:
                    label_count[label] += 1
    return label_count

def split_data(files, label_count):
    diff = label_count['reliable'] - label_count['unreliable']
    if diff == 0:
        print("Already balanced")
        return
    if diff > 0:
        print(f"Removing {abs(diff):,} articles from reliable")
    else:
        print(f"Removing {abs(diff):,} articles from unreliable")

    n_files = len(files)
    n_to_remove = abs(diff) // n_files

    print(f"Removing {n_to_remove:,} articles from each file")

    for i, file_ in enumerate(files):
        print(f"Processing file {i} of {n_files}", end='\r')
        with open(tokens_folder + file_, 'r') as f:
            with open(save_path + "fifty_" + file_, 'w') as f2:
                reader = csv.reader(f)
                writer = csv.writer(f2)
                
                n_removed = 0
                for row in reader:
                    if n_removed <= n_to_remove:
                        label = label_dict[row[0]]
                        if label == 'reliable' and diff > 0:
                            n_removed += 1
                            continue
                        if label == 'unreliable' and diff < 0:
                            n_removed += 1
                            continue

                    writer.writerow(row)

if __name__ == '__main__':
    files = os.listdir(tokens_folder)
    label_count = count_label(files)
    print(label_count)
    split_data(files, label_count)

    print(count_label(os.listdir(save_path), folder = save_path))
    # {'reliable': 3570431, 'unreliable': 3570094}