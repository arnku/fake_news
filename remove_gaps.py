import os
import csv
import shutil

csv.field_size_limit(1310720)

def get_missing_indecies(files, header = True):
    print("Getting missing indices")
    missing_indices = []
    last_row = -1
    for file_ in files:
        print(file_)
        with open(file_, 'r') as f:
            reader = csv.reader(f)
            if header:
                next(reader)
            
            for row in reader:
                id_ = int(row[0])
                if id_ > last_row + 1:
                    missing_indices.extend(list(range(last_row + 1, id_)))
                last_row = id_
    return missing_indices

def remove_indecies(folder, missing_indices, header = True):
    '''
    Goes through all files and removes the given indices
    '''
    print("Removing indices")
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

    shutil.rmtree(folder)        
    os.rename("tmp", folder)
    
def remove_relative_gaps(folder1, folder2, header=True):
    '''
    Goes through all files and makes sure that if a gap occurs in the first folder, it also occurs in the second folder
    '''
    print("Removing relative gaps")
    # sort files
    files1 = sorted(os.listdir(folder1), key=lambda x: int(x.split('_')[-1].split('.')[0]))
    files2 = sorted(os.listdir(folder2), key=lambda x: int(x.split('_')[-1].split('.')[0]))

    missing_indices = []
    missing_indices.extend(get_missing_indecies([folder1 + file_ for file_ in files1], header))
    missing_indices.extend(get_missing_indecies([folder2 + file_ for file_ in files2], header))
    
    missing_indices = sorted(list(set(missing_indices)))
    print(missing_indices)

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
    first_time = True
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
                    row[0] = n
                    n += 1
                    writer.writerow(row)
    
    shutil.rmtree(folder)
    os.rename("tmp", folder)


def remove_to_size(folder1, folder2):
    '''
    Make sure that there are equal number of articles in both folders
    '''
    files1 = sorted(os.listdir(folder1), key=lambda x: int(x.split('_')[-1].split('.')[0]), reverse=True)
    files2 = sorted(os.listdir(folder2), key=lambda x: int(x.split('_')[-1].split('.')[0]), reverse=True)

    n1_max = 0
    n2_max = 0
    with open(folder1 + files1[0], 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            n1_max = int(row[0])
    with open(folder2 + files2[0], 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            n2_max = int(row[0])
    n_max = min(n1_max, n2_max)
    print(n_max)

    os.makedirs("tmp")
    for file_ in files1:
        with open(folder1 + file_, 'r') as f:
            with open("tmp/" + file_, 'w') as g:
                reader = csv.reader(f)
                writer = csv.writer(g)
                header = next(reader)
                writer.writerow(header)
                for row in reader:
                    if int(row[0]) > n_max:
                        continue
                    writer.writerow(row)
    shutil.rmtree(folder1)
    os.rename("tmp", folder1)

    os.makedirs("tmp")
    for file_ in files2:
        with open(folder2 + file_, 'r') as f:
            with open("tmp/" + file_, 'w') as g:
                reader = csv.reader(f)
                writer = csv.writer(g)
                header = next(reader)
                writer.writerow(header)
                for row in reader:
                    if int(row[0]) > n_max:
                        continue
                    writer.writerow(row)
    shutil.rmtree(folder2)
    os.rename("tmp", folder2)

def remove_empty_files(folder):
    files = os.listdir(folder)
    for file_ in files:
        with open(folder + file_, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            if not list(reader):
                os.remove(folder + file_)

if __name__ == "__main__":
    folder1 = "tf-idf/"
    folder2 = "features/"
    remove_relative_gaps(folder1,folder2)
    remove_gaps(folder1)
    remove_gaps(folder2)
    remove_to_size(folder1, folder2)
    remove_empty_files(folder1)
    remove_empty_files(folder2)