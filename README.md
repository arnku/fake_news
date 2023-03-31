This code is only tested on MacOS and Linux. It will not work on windows as we have used '/' for folders.
Specifically a macbook pro 14" m1 16GB, and a Linux machine with an AMD Ryzen cpu with 16-threads and 16GB RAM. It is a good idea to have at least 100GB of hard-disc space empty if hte whole dataset is processed. Some of the processes will use all available threads. 

# Training
To be able to train on the FakeNewsCorpus, the data must first be cleaned and processed.

## Cleaning and preprocessing
The csv file from FakeNewsCorpus must be unzipped and placed in the root folder of the project, and must be named 'FakeNewsCorpus.csv'
Following is the order to run the scripts and what variables inside of the scripts should be set to.

First the data set musst be split into smaller chunks for it to use less memory while processing. The defualt size for this is chunks of 20.000 articels, but can be changed by setting the 'split_size' variable. This step also removes articles only consisting of non-latin characters. 
**split_files.py** Splits 'FakeNewsCorpus.csv' into smaller chunks, and saves them in 'splits/'

As the FakeNewsCorpus is not totally random in its distribution of labels, the labels are needed to be randomized.
This is run already at this step, as it is then possible to delete some of the chunks afterwards, if a smaller data set is desired, without changing the distribution of the labels.

**article_randomizer.py** Makes a same number of chunks, but randomizes articles position in them.
Input and save folders should be set to:
```
input_folder = 'splits/'
save_folder = 'splits_randomized/' 
```

Most of the cleaning processed is then applied. This step will take a lot of CPU resources, so it is not recommended to run other programs while it runs.
This steps removes files that it has processed. This is so that it does not have to start over if the process is interrupted. 

**splits_2_clean.py** Cleans the data set. 
Input and output folders should be set to:
```
splits_folder = 'splits/'
save_path = 'tokens/'
```

The data set is not garanteed to be balanced between reliable and unreliable articles. This step makes sure that there are around as many relaiable as unreliable articles.
This step is run after *splits_2_clean.py* as it will process faster on the smaller files, but can be run at any time before. 

**50-50_splitter.py** Deletes reliable or unreliable articles until they are almost balanced.
Input and output folders should be set to:
```
tokens_folder = 'tokens/'
save_path = '50-50_split/'
```
In addition to this, what is considered relaible or unreliable can be changed in 'label_dict'.
```
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
```

The files are now mostly done being moved around and deleted, so now is a good time to give each article a unique number to be able to keep track of them.

**numerate_articles.py** Gives each article a unique number in order. This number is stored at the first index of each article.
Input and output folders should be set to:
```
tokens_folder = '50-50_split/'
save_folder = 'numerated/'
```

The tf-idf is then found for each article, and the total df is also saved.

**tf-idf.py** calculated tf-idf and df.
Input and output folders should be set to:
```
tokens_folder = 'numerated/'
save_folder = 'tf-idf/'
```
If it is the first time running the training pipleine, 'create_new_dfs' should be set to 'True'. 
This will create/overwrite the 'dfs.csv' file that contains the top 10.000 across all articles.

The data files for a very simple bag of words model is also created. This is run after *tf-idf.py* as it requires the *dfs.csv* file.

**bagowords.py** Uses the top 10.000 words to create a bag of words, also counts how many words in each article is inside and outside the bag.
Input and output folders should be set to:
```
dfs_file = 'dfs.csv'
tokens_folder = '50-50_split/'
output_folder = 'bagowords/'
```

The advnaced model also needs some extra features. These are extracted here. This process takes a very long time as it runs sentiment analysis. It is recommended to have a GPU for this step, as the sentiment analysis model is based on either PyTourch or Tensorflow, which both can take advantage of a GPU.

**get_features.py** Calcualtes Lix, Sentiment, and percent out of bag, for each article.
Input and output folders should be set to:
```
words_file = 'dfs.csv'
tokens_folder = 'numerated/'
output_folder = 'features/'
```

The prior two processes most likely will have discarded some articles as they could not be processed. To ensure that the articles still are in order, the removed articles are noted, and removed from both *features/* and *tf-idf/*. They should now contain the same articles. Then the articles are renumbered so they are in order. 

**remove_gaps.py**
Folders to be changed should be set to:
```
folder1 = "tf-idf/"
folder2 = "features/"
```

We then change to tf-idf's to be in the form of a sparce matrix. This is to save memory later. 

**sparce_matrix.py** Changes format to be able to be easilly parsed to a sparce matrix. 
Input and output folders should be set to:
```
words_file = 'dfs.csv'
tf_idf_folder = 'tf-idf/'
save_folder = 'reduced_matrix/'
```

All the data needed for training is now done.

## Training the models

### Model A
Train model A. This model is based on the number of words inside and outside the top 10.000 words.

**model_a_train.py** 
Input folders should be set to:
```
bago_folder = 'bagowords/'
```
Saves the model as 'model_a.pkl'.
If 'label_dict' was changed earlier, it should then also be changed accordingly here. 'False' is unreliable, and 'True' is reliable.
```
label_dict = {
    'bias': False, 
    'satire': False,
    'rumor': False,
    'conspiracy': False,
    'hate': False,
    'fake': False,
    'junksci': False,
    'unreliable': False,
    'clickbait': False,
    'reliable': True,
    'political': True
    }
```

### Model B
Train model B. This model is based on the sparce matrix representation of a bag of words.

**model_b_train.py**
Input folders should be set to:
```
sparce_matrix_folder = 'reduced_matrix/'
dfs_file = 'dfs.csv'
```
Saves the model as 'model_b.pkl'.
If 'label_dict' was changed earlier, it should then also be changed accordingly here. 'False' is unreliable, and 'True' is reliable.
```
label_dict = {
    'bias': False,
    'satire': False,
    'rumor': False,
    'conspiracy': False,
    'hate': False,
    'fake': False,
    'junksci': False,
    'unreliable': False,
    'clickbait': False,
    'reliable': True,
    'political': True,
    }
```

### Model Advanced
Train the advanced model. This model is based on tf-idf in a sparce matrix representation together with some features. 

**model_adv_train.py**
Input folders should be set to:
```
sparce_matrix_folder = 'reduced_matrix/'
features_folder = 'features/'
dfs_file = 'dfs.csv'
```
Saves the model as 'model_adv.pkl'.
If 'label_dict' was changed earlier, it should then also be changed accordingly here. 'False' is unreliable, and 'True' is reliable.
```
label_dict = {
    'bias': False,
    'satire': False,
    'rumor': False,
    'conspiracy': False,
    'hate': False,
    'fake': False,
    'junksci': False,
    'unreliable': False,
    'clickbait': False,
    'reliable': True,
    'political': True
    }
```

# Predicting on LIAR
To be able to predict on the LIAR, the data must first be cleaned and processed.
If folders from running the training pipeline is still present, these folders should be deleted. This is to ensure that the data is not mixed up.
'dfs.csv', 'model_a.pkl', 'model_b.pkl', 'model_adv.pkl' should be kept.

## Cleaning the data
The test tsv file from LIAR must be unzipped and placed in the root folder of the project, and must be named 'test.tsv'
Following is the order to run the scripts and what variables inside of the scripts should be set to.

The tsv file is split into smaller chunks if necessary. This is done to save memory. The more important part of this step is to convert it to be in the same overall structure as the FakeNewsCorpus.

**split_files_liar.py** Splits 'test.tsv' into smaller chunks, and saves them in 'splits/'
Input and output folders should be set to:
```
save_path = 'splits/'
file_name = 'test.tsv'
```

Most of the cleaning processed is then applied. This steps removes files that it has processed. This is so that it does not have to start over if the process is interrupted. 

**splits_2_clean.py** Cleans the data set. 
Input and output folders should be set to:
```
splits_folder = 'splits/'
save_path = 'tokens/'
```

The data files for a very simple bag of words model is also created. This is run after *tf-idf.py* as it requires the *dfs.csv* file.

**bagowords.py** Uses the top 10.000 words to create a bag of words, also counts how many words in each article is inside and outside the bag.
Input and output folders should be set to:
```
dfs_file = 'dfs.csv'
tokens_folder = 'tokens/'
output_folder = 'bagowords/'
```

The files are now mostly done being moved around and deleted, so now is a good time to give each article a unique number to be able to keep track of them.

**numerate_articles.py** Gives each article a unique number in order. This number is stored at the first index of each article.
Input and output folders should be set to:
```
tokens_folder = 'tokens/'
save_folder = 'numerated/'
header = False
```

The tf-idf is then found for each article, and the total df is also saved.

**tf-idf.py** calculated tf-idf and df.
Input and output folders should be set to:
```
tokens_folder = 'numerated/'
save_folder = 'tf-idf/'
create_new_dfs = False
```

The advnaced model also needs some extra features. These are extracted here. This process takes a very long time as it runs sentiment analysis. It is recommended to have a GPU for this step, as the sentiment analysis model is based on either PyTourch or Tensorflow, which both can take advantage of a GPU.

**get_features.py** Calcualtes Lix, Sentiment, and percent out of bag, for each article.
Input and output folders should be set to:
```
words_file = 'dfs.csv'
tokens_folder = 'numerated/'
output_folder = 'features/'
```

We then change to tf-idf's to be in the form of a sparce matrix. This is to save memory later. 

**sparce_matrix.py** Changes format to be able to be easilly parsed to a sparce matrix. 
Input and output folders should be set to:
```
words_file = 'dfs.csv'
tf_idf_folder = 'tf-idf/'
save_folder = 'reduced_matrix/'
```

The prior two processes most likely will have discarded some articles as they could not be processed. To ensure that the articles still are in order, the removed articles are noted, and removed from both *features/* and *tf-idf/*. They should now contain the same articles. Then the articles are renumbered so they are in order. 

**remove_gaps.py**
Folders to be changed should be set to:
```
folder1 = "tf-idf/"
folder2 = "features/"
```

All the data is now ready to be predicted on.

## Predicting on the data

### Model A
**model_a_predict.py**
The input folders should be set to:
```
bago_folder = 'bagowords/'
```
If 'label_dict' was changed earlier, it should then also be changed accordingly here. 'False' is unreliable, and 'True' is reliable.
The meaning of the labels from LIAR is also set here.
```
label_dict = {
    'bias': False,
    'satire': False,
    'rumor': False,
    'conspiracy': False,
    'hate': False,
    'fake': False,
    'junksci': False,
    'unreliable': False,
    'clickbait': False,
    'reliable': True,
    'political': True,

    'pants-fire': False,
    'false': False,
    'half-true': False,
    'barely-true': False,
    'mostly-true': False,
    'true': True,
    }
```

### Model B
**model_b_predict.py**
The input folders should be set to:
```
sparce_matrix_folder = 'reduced_matrix/'
dfs_file = 'dfs.csv'
```
If 'label_dict' was changed earlier, it should then also be changed accordingly here. 'False' is unreliable, and 'True' is reliable.
The meaning of the labels from LIAR is also set here.
```
label_dict = {
    'bias': False,
    'satire': False,
    'rumor': False,
    'conspiracy': False,
    'hate': False,
    'fake': False,
    'junksci': False,
    'unreliable': False,
    'clickbait': False,
    'reliable': True,
    'political': True,

    'pants-fire': False,
    'false': False,
    'half-true': False,
    'barely-true': False,
    'mostly-true': False,
    'true': True,
    }
```

### Model Adv
**model_adv_predict.py**
The input folders should be set to:
```
sparce_matrix_folder = 'reduced_matrix/'
features_folder = 'features/'
dfs_file = 'dfs.csv'
```
If 'label_dict' was changed earlier, it should then also be changed accordingly here. 'False' is unreliable, and 'True' is reliable.
The meaning of the labels from LIAR is also set here.
```
label_dict = {
    'bias': False,
    'satire': False,
    'rumor': False,
    'conspiracy': False,
    'hate': False,
    'fake': False,
    'junksci': False,
    'unreliable': False,
    'clickbait': False,
    'reliable': True,
    'political': True,

    'pants-fire': False,
    'false': False,
    'half-true': False,
    'barely-true': False,
    'mostly-true': False,
    'true': True,
    }
```

# Libraries
The used Python libraries and their versions:
```
anyio==3.6.2
  - idna [required: >=2.8, installed: 3.4]
  - sniffio [required: >=1.1, installed: 1.3.0]
argon2-cffi==21.3.0
  - argon2-cffi-bindings [required: Any, installed: 21.2.0]
    - cffi [required: >=1.0.1, installed: 1.15.1]
      - pycparser [required: Any, installed: 2.21]
beautifulsoup4==4.11.2
  - soupsieve [required: >1.2, installed: 2.3.2.post1]
bleach==6.0.0
  - six [required: >=1.9.0, installed: 1.15.0]
  - webencodings [required: Any, installed: 0.5.1]
certifi==2022.12.7
charset-normalizer==3.0.1
comm==0.1.2
  - traitlets [required: >=5.3, installed: 5.9.0]
confuse==2.0.0
  - pyyaml [required: Any, installed: 6.0]
debugpy==1.6.6
defusedxml==0.7.1
dicttoxml==1.7.15
fqdn==1.5.1
future==0.18.2
ipython==8.9.0
  - appnope [required: Any, installed: 0.1.3]
  - backcall [required: Any, installed: 0.2.0]
  - decorator [required: Any, installed: 5.1.1]
  - jedi [required: >=0.16, installed: 0.18.2]
    - parso [required: >=0.8.0,<0.9.0, installed: 0.8.3]
  - matplotlib-inline [required: Any, installed: 0.1.6]
    - traitlets [required: Any, installed: 5.9.0]
  - pexpect [required: >4.3, installed: 4.8.0]
    - ptyprocess [required: >=0.5, installed: 0.7.0]
  - pickleshare [required: Any, installed: 0.7.5]
  - prompt-toolkit [required: >=3.0.30,<3.1.0, installed: 3.0.36]
    - wcwidth [required: Any, installed: 0.2.6]
  - pygments [required: >=2.4.0, installed: 2.14.0]
  - stack-data [required: Any, installed: 0.6.2]
    - asttokens [required: >=2.1.0, installed: 2.2.1]
      - six [required: Any, installed: 1.15.0]
    - executing [required: >=1.2.0, installed: 1.2.0]
    - pure-eval [required: Any, installed: 0.2.2]
  - traitlets [required: >=5, installed: 5.9.0]
ipython-genutils==0.2.0
isoduration==20.11.0
  - arrow [required: >=0.15.0, installed: 1.2.3]
    - python-dateutil [required: >=2.7.0, installed: 2.8.2]
      - six [required: >=1.5, installed: 1.15.0]
jellyfish==0.9.0
Jinja2==3.1.2
  - MarkupSafe [required: >=2.0, installed: 2.1.2]
jsonpointer==2.3
jupyter-client==8.0.2
  - importlib-metadata [required: >=4.8.3, installed: 6.0.0]
    - zipp [required: >=0.5, installed: 3.12.1]
  - jupyter-core [required: >=4.12,!=5.0.*, installed: 5.2.0]
    - platformdirs [required: >=2.5, installed: 3.0.0]
    - traitlets [required: >=5.3, installed: 5.9.0]
  - python-dateutil [required: >=2.8.2, installed: 2.8.2]
    - six [required: >=1.5, installed: 1.15.0]
  - pyzmq [required: >=23.0, installed: 25.0.0]
  - tornado [required: >=6.2, installed: 6.2]
  - traitlets [required: >=5.3, installed: 5.9.0]
jupyter-server-terminals==0.4.4
  - terminado [required: >=0.8.3, installed: 0.17.1]
    - ptyprocess [required: Any, installed: 0.7.0]
    - tornado [required: >=6.1.0, installed: 6.2]
jupyterlab-pygments==0.2.2
jupyterlab-widgets==3.0.5
macholib==1.15.2
  - altgraph [required: >=0.15, installed: 0.17.2]
mediafile==0.11.0
  - mutagen [required: >=1.46, installed: 1.46.0]
  - six [required: >=1.9, installed: 1.15.0]
mistune==2.0.5
munkres==1.1.4
musicbrainzngs==0.7.1
nbformat==5.7.3
  - fastjsonschema [required: Any, installed: 2.16.2]
  - jsonschema [required: >=2.6, installed: 4.17.3]
    - attrs [required: >=17.4.0, installed: 22.2.0]
    - pyrsistent [required: >=0.14.0,!=0.17.2,!=0.17.1,!=0.17.0, installed: 0.19.3]
  - jupyter-core [required: Any, installed: 5.2.0]
    - platformdirs [required: >=2.5, installed: 3.0.0]
    - traitlets [required: >=5.3, installed: 5.9.0]
  - traitlets [required: >=5.1, installed: 5.9.0]
nest-asyncio==1.5.6
pandocfilters==1.5.0
pip==23.0
pipdeptree==2.5.1
prometheus-client==0.16.0
psutil==5.9.4
python-json-logger==2.0.4
pytz==2022.7.1
QtPy==2.3.0
  - packaging [required: Any, installed: 23.0]
rfc3339-validator==0.1.4
  - six [required: Any, installed: 1.15.0]
rfc3986-validator==0.1.1
Send2Trash==1.8.0
setuptools==58.0.4
tinycss2==1.2.1
  - webencodings [required: >=0.4, installed: 0.5.1]
typing-extensions==4.4.0
Unidecode==1.3.6
uri-template==1.2.0
urllib3==1.26.14
webcolors==1.12
websocket-client==1.5.1
wheel==0.37.0
widgetsnbextension==4.0.5
```
