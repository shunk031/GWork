# G Work

## Install requirement modules

``` shell
$ pip install -r python_requirements.txt
```

## Collect news article from gunosy

``` shell
$ cd scripts
$ python crawl_page.py CATEGORY # specify article category

```

The collected articles are stored in `data` of the current directory.

## Preprocess

### Make single csv file

Make each article data to one CSV file for each category. The CSV file is stored in `GClassifier/dataset/row`.

``` shell
$ cd scripts
$ python make_single_file.py all # specify article category or all
```

### Wakatigaking

Do wakatigaki data and format it. Output CSV file is stored in `GClassifier/dataset/preprocess`. 

``` shell
$ cd GClassifier
$ python g_preprocess.py all --wakati_type mecab-noun

# if you use n-gram
$ python g_preprocess.py all --wakati_type n-gram --ngram_n 2
```

### Train Naive Bayes model and dump it.

Train Naive Bayes model using the wakatigaking data and dump it to `GClassifier/naive_bayes_model.pkl`.

``` shell
$ cd GClassifier
$ python dump_classifier.py mecab-noun_all
```

## Run Predict news category server

Run the server and enter gunosy article URL.

``` shell
$ python manage.py runserver
```

## Model validation

We evaluated classifier using 5-fold cross validation. The result is [here](https://github.com/shunk031/GWork/blob/master/GClassifier/README.md)
