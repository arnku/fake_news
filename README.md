! This code is only tested on MacOS and Linux. It will not work on windows as we have used '/' for folders.

# Rækkefølge

**split_files.py** splitter datesæt til mindre filer.

**token_randomizer** randomizes the files

**splits_2_clean** cleaner de mindre filer.

**50-50_splitter**

**tf-idf**

**sparce_matrix**



# Rækkefølge for liar

**split_files_liar.py**, 

**splits_2_clean** , splits_folder = 'splits/'

**numerate_articles.py**, numerate('tokens/', 'numerated/', header = False)

**tf-idf**, tokens_folder = 'numerated/', create_new_dfs = False

**get_features.py** tokens_folder = 'numerated/', words_file = 'dfs.csv', output_folder = 'features/'

**sparce_matrix.py** words_file = 'dfs.csv', tf_idf_folder = 'tf-idf/', save_folder = 'reduced_matrix/'

**remove_gaps.py** folder1 = "tf-idf/", folder2 = "features/"

**bagowords.py**
