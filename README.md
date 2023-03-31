This code is only tested on MacOS and Linux. It will not work on windows as we have used '/' for folders.
Specifically a macbook pro 14" m1 16GB, and a Linux machine with an AMD Ryzen cpu with 16-threads and 16GB RAM. It is a good idea to have at least 100GB of hard-disc space empty if hte whole dataset is processed. Some of the processes will use all available threads. 

# Training
To be able to train on the FakeNewsCorpus, the data must first be cleaned and processed.

## Cleaning and preprocessing
The csv file from FakeNewsCorpus must be unzipped and placed in the root folder of the project, and must be named ´FakeNewsCorpus.csv´
Following is the order to run the scripts and what variables inside of the scripts should be set to.

First the data set musst be split into smaller chunks for it to use less memory while processing. The defualt size for this is chunks of 20.000 articels, but can be changed by setting the ´split_size´ variable. This step also removes articles only consisting of non-latin characters. 
**split_files.py** Splits ´FakeNewsCorpus.csv´ into smaller chunks, and saves them in ´splits/´

As the FakeNewsCorpus is not totally random in its distribution of labels, the labels are needed to be randomized.
This is run already at this step, as it is then possible to delete some of the chunks afterwards, if a smaller data set is desired, without changing the distribution of the labels.
**article_randomizer.py** Makes a same number of chunks, but randomizes articles position in them.
Input and save folders should be set to:
´´´
input_folder = 'splits/'
save_folder = 'splits_randomized/' 
´´´

Most of the cleaning processed is then applied. This step will take a lot of CPU resources, so it is not recommended to run other programs while it runs.
This steps removes files that it has processed. This is so that it does not have to start over if the process is interrupted. 
**splits_2_clean.py** Cleans the data set. 
Input and output folders should be set to:
´´´
splits_folder = 'splits/'
save_path = 'tokens/'
´´´

The data set is not garanteed to be balanced between reliable and unreliable articles. This step makes sure that there are around as many relaiable as unreliable articles.
This step is run after *splits_2_clean.py* as it will process faster on the smaller files, but can be run at any time before. 
**50-50_splitter.py** Deletes reliable or unreliable articles until they are almost balanced.
Input and output folders should be set to:
´´´
tokens_folder = 'tokens/'
save_path = '50-50_split/'
´´´
In addition to this, what is considered relaible or unreliable can be changed in ´label_dict´.
´´´
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
´´´

The files are now mostly done being moved around and deleted, so now is a good time to give each article a unique number to be able to keep track of them.
**numerate_articles.py** Gives each article a unique number in order. This number is stored at the first index of each article.
Input and output folders should be set to:
´´´
tokens_folder = '50-50_split/'
save_folder = 'numerated/'
´´´

The tf-idf is then found for each article, and the total df is also saved.
**tf-idf.py** calculated tf-idf and df.
Input and output folders should be set to:
´´´
tokens_folder = 'numerated/'
save_folder = 'tf-idf/'
´´´
If it is the first time running the training pipleine, ´create_new_dfs´ should be set to ´True´. 
This will create/overwrite the ´dfs.csv´ file that contains the top 10.000 across all articles.

The data files for a very simple bag of words model is also created. This is run after *tf-idf.py* as it requires the *dfs.csv* file.
**bagowords.py** Uses the top 10.000 words to create a bag of words, also counts how many words in each article is inside and outside the bag.
Input and output folders should be set to:
´´´
dfs_file = 'dfs.csv'
tokens_folder = 'numerated/'
output_folder = 'bagowords/'
´´´

The advnaced model also needs some extra features. These are extracted here. This process takes a very long time as it runs sentiment analysis. It is recommended to have a GPU for this step, as the sentiment analysis model is based on either PyTourch or Tensorflow, which both can take advantage of a GPU.
**get_features.py** Calcualtes Lix, Sentiment, and percent out of bag, for each article.
Input and output folders should be set to:
´´´
words_file = 'dfs.csv'
tokens_folder = 'numerated/'
output_folder = 'features/'
´´´

The prior two processes most likely will have discarded some articles as they could not be processed. To ensure that the articles still are in order, the removed articles are noted, and removed from both *features/* and *tf-idf/*. They should now contain the same articles. Then the articles are renumbered so they are in order. 
**remove_gaps.py**
Folders to be changed should be set to:
´´´
folder1 = "tf-idf/"
folder2 = "features/"
´´´

We then change to tf-idf's to be in the form of a sparce matrix. This is to save memory later. 
**sparce_matrix.py** Changes format to be able to be easilly parsed to a sparce matrix. 
Input and output folders should be set to:
´´´
words_file = 'dfs.csv'
tf_idf_folder = 'tf-idf/'
save_folder = 'reduced_matrix/'
´´´

All the data needed for training is now done.

## Training the models

### Model A

**very_nieve_model.py**


### Model B

### Model Advanced

# Predicting

# Rækkefølge for liar

**split_files_liar.py**, 

**bagowords.py**, header = True

**splits_2_clean** , splits_folder = 'splits/'

**numerate_articles.py**, numerate('tokens/', 'numerated/', header = False)

**tf-idf**, tokens_folder = 'numerated/', create_new_dfs = False

**get_features.py** tokens_folder = 'numerated/', words_file = 'dfs.csv', output_folder = 'features/'

**sparce_matrix.py** words_file = 'dfs.csv', tf_idf_folder = 'tf-idf/', save_folder = 'reduced_matrix/'

**remove_gaps.py** folder1 = "tf-idf/", folder2 = "features/"





# Libraries
