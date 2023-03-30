import os
import csv

csv.field_size_limit(1310720)

def get_missing_indecies(files, header = True):
    missing_indices = []
    for file_ in files:
        print(file_)
        with open(file_, 'r') as f:
            reader = csv.reader(f)
            if header:
                next(reader)
            
            last_row = -1
            for row in reader:
                id_ = int(row[0])
                if id_ > last_row + 1:
                    missing_indices.append(id_)
                last_row = id_
    return missing_indices

def remove_indecies(folder, missing_indices, header = True):
    '''
    Goes through all files and removes the given indices
    '''
    files = os.listdir(folder)
    os.makedirs("tmp")
    for file_ in files:
        print(file_)
        with open(folder + file_, 'r') as f:
            with open("tmp/" + file_, 'w') as g:
                reader = csv.reader(f)
                writer = csv.writer(g)
                if header:
                    header = next(reader)
                    writer.writerow(header)
                for row in reader:
                    id_ = int(row[0])
                    if id_ in missing_indices:
                        continue
                    writer.writerow(row)
    os.rename("tmp", folder)
    
def remove_relative_gaps(folder1, folder2, header=True):
    '''
    Goes through all files and makes sure that if a gap occurs in the first folder, it also occurs in the second folder
    '''
    # sort files
    files1 = sorted(os.listdir(folder1), key=lambda x: int(x.split('_')[-1].split('.')[0]))
    files2 = sorted(os.listdir(folder2), key=lambda x: int(x.split('_')[-1].split('.')[0]))

    missing_indices = []
    missing_indices.extend(get_missing_indecies([folder1 + file_ for file_ in files1], header))
    missing_indices.extend(get_missing_indecies([folder2 + file_ for file_ in files2], header))
    
    missing_indices = sorted(list(set(missing_indices)))

    remove_indecies(folder1, missing_indices, header)
    remove_indecies(folder2, missing_indices, header)

def remove_gaps(folder, header = True):
    '''
    Goes through all files and removes gaps in the article ids
    '''
    # sort files
    files = sorted(os.listdir(folder), key=lambda x: int(x.split('_')[-1].split('.')[0]))
    os.makedirs("tmp")
    n = 0
    last_n = 0
    for file_ in files:
        print(file_)
        with open(folder + file_, 'r') as f:
            with open("tmp/" + file_, 'w') as g:
                reader = csv.reader(f)
                writer = csv.writer(g)
                if header:
                    header = next(reader)
                    writer.writerow(header)
                for row in reader:
                    id_ = int(row[0])
                    if id_ > last_n:
                        n += 1
                        last_n = id_
                    row[0] = n
                    writer.writerow(row)
    os.rename("tmp", folder)
    
