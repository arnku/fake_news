import os
import csv

csv.field_size_limit(1310720)

def numerate(input_folder, output_folder, header = True):
    os.makedirs(output_folder, exist_ok=True)
    n = 0
    # sort files
    files = sorted(os.listdir(input_folder), key=lambda x: int(x.split('_')[-1].split('.')[0]))
    for file_ in files:
        print(file_)
        with open(input_folder + file_, 'r') as f:
            with open(output_folder + file_, 'w') as f2:
                reader = csv.reader(f, delimiter=',')
                writer = csv.writer(f2, delimiter=',')
                
                if header:
                    header = next(reader)
                    a = ['i']
                    a.extend(header)
                    writer.writerow(a)
                
                for row in reader:
                    m = [n]
                    m.extend(row)
                    writer.writerow(m)
                    n += 1

if __name__ == '__main__':
    numerate('50-50_split/', 'numerated/', header = False)