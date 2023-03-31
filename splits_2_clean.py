'''
This script takes the splits folder and cleans the text in the content column.
It then saves the cleaned text in the tokens folder.

Should be run after split_files.py

Does not take a lot of ram, but does use all cpu cores.
'''

import os
import cleantext
from multiprocessing import Pool
from time import time
import csv
import regex as re

splits_folder = 'splits_randomized/'
save_path = 'tokens/'

csv.field_size_limit(1310720)
os.makedirs(save_path, exist_ok=True)

valid_labels = ['bias', 'satire', 'rumor', 'conspiracy', 'hate', 'fake', 'junksci', 'unreliable', 'clickbait', 'reliable', 'political', 'false', 'half-true', 'pants-fire', 'true', 'barely-true', 'mostly-true']

# taken hostname, domainname, tld from URL regex below
EMAIL_REGEX = re.compile(
    r"(?:^|(?<=[^\w@.)]))([\w+-](\.(?!\.))?)*?[\w+-](@|[(<{\[]at[)>}\]])(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))",
    flags=re.IGNORECASE | re.UNICODE,
)

# for more information: https://github.com/jfilter/clean-text/issues/10
PHONE_REGEX = re.compile(
    r"((?:^|(?<=[^\w)]))(((\+?[01])|(\+\d{2}))[ .-]?)?(\(?\d{3,4}\)?/?[ .-]?)?(\d{3}[ .-]?\d{4})(\s?(?:ext\.?|[#x-])\s?\d{2,6})?(?:$|(?=\W)))|\+?\d{4,5}[ .-/]\d{6,9}"
)

NUMBERS_REGEX = re.compile(
    r"(?:^|(?<=[^\w,.]))[+–-]?(([1-9]\d{0,2}(,\d{3})+(\.\d*)?)|([1-9]\d{0,2}([ .]\d{3})+(,\d*)?)|(\d*?[.,]\d+)|\d+)(?:$|(?=\b))"
)

# source: https://gist.github.com/dperini/729294
# @jfilter: I guess it was changed
URL_REGEX = re.compile(
    r"(?:^|(?<![\w\/\.]))"
    # protocol identifier
    # r"(?:(?:https?|ftp)://)"  <-- alt?
    r"(?:(?:https?:\/\/|ftp:\/\/|www\d{0,3}\.))"
    # user:pass authentication
    r"(?:\S+(?::\S*)?@)?" r"(?:"
    # IP address exclusion
    # private & local networks
    r"(?!(?:10|127)(?:\.\d{1,3}){3})"
    r"(?!(?:169\.254|192\.168)(?:\.\d{1,3}){2})"
    r"(?!172\.(?:1[6-9]|2\d|3[0-1])(?:\.\d{1,3}){2})"
    # IP address dotted notation octets
    # excludes loopback network 0.0.0.0
    # excludes reserved space >= 224.0.0.0
    # excludes network & broadcast addresses
    # (first & last IP address of each class)
    r"(?:[1-9]\d?|1\d\d|2[01]\d|22[0-3])"
    r"(?:\.(?:1?\d{1,2}|2[0-4]\d|25[0-5])){2}"
    r"(?:\.(?:[1-9]\d?|1\d\d|2[0-4]\d|25[0-4]))"
    r"|"
    # host name
    r"(?:(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)"
    # domain name
    r"(?:\.(?:[a-z\\u00a1-\\uffff0-9]-?)*[a-z\\u00a1-\\uffff0-9]+)*"
    # TLD identifier
    r"(?:\.(?:[a-z\\u00a1-\\uffff]{2,}))" r"|" r"(?:(localhost))" r")"
    # port number
    r"(?::\d{2,5})?"
    # resource path
    r"(?:\/[^\)\]\}\s]*)?",
    # r"(?:$|(?![\w?!+&\/\)]))",
    # @jfilter: I removed the line above from the regex because I don't understand what it is used for, maybe it was useful?
    # But I made sure that it does not include ), ] and } in the URL.
    flags=re.UNICODE | re.IGNORECASE,
)


def process_file(split_path):
    header = False

    start_time = time()
    error_count = 0
    with open(splits_folder + split_path, 'r') as input_file:
        with open(save_path + "token_" + split_path, 'w') as output_file:
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)

            if header:
                header = next(reader) # skip header
                writer.writerow(header)

            for row in reader:
                if row[0] not in valid_labels:
                    continue
                content = URL_REGEX.sub('URL', row[1])
                content = EMAIL_REGEX.sub('EMAIL', content)
                content = PHONE_REGEX.sub('PHONE', content)
                content = NUMBERS_REGEX.sub('NUMBER', content)
                
                content = cleantext.clean_words(content, clean_all= True)
                writer.writerow((row[0],' '.join(content)))

    os.remove(splits_folder + split_path)
    print(f"Processed {split_path} in {round((time() - start_time)/60,3)} minutes with {error_count} errors.")

if __name__ == '__main__':
    with Pool() as p:
        p.map(process_file, os.listdir(splits_folder))
