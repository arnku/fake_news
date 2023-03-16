import os
import csv
import cleantext

save_path = 'tokens/'
splits_folder = 'splits/'

os.makedirs(save_path, exist_ok=True)
csv.field_size_limit(1310720)

for split_path in os.listdir(splits_folder):
    print(split_path)
    
    tokens = []
    input(splits_folder + split_path)
    with open(splits_folder + split_path, 'r') as r:
        reader = csv.reader(r)
        header = next(reader)

        for row in reader:
            try:
                content = row[5]
                content = cleantext.clean_words(content)
                tokens.append((row[3],' '.join(content)))
            except:
                print(row)
                pass
    
    with open(save_path + split_path, 'w') as w:
        writer = csv.writer(w)
        writer.writerow((header[3], header[5]))
        writer.writerows(tokens)