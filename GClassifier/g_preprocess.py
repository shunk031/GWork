# -*- coding: utf-8 -*-

import argparse
import os
import MeCab
import pandas as pd

from tqdm import tqdm

DATASET_ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'dataset')
ROW_DATASET_DIR = os.path.join(DATASET_ROOT_DIR, 'row')
PREPROCESSED_DATASET_DIR = os.path.join(DATASET_ROOT_DIR, 'preprocessed')

CATEGORIES = ["entertainment", "sports", "interesting", "domestic", "overseas", "column", "science", "gourmet"]


class PreprocessDataset:

    WAKATI_TYPE = ["mecab-noun", "n-gram"]

    def __init__(self, wakati_type='mecab-noun', ngram_n=None):
        self._check_wakati_type(wakati_type)

        self.wakati_type = wakati_type
        self.ngram_n = ngram_n
        self.mt = MeCab.Tagger("-Ochasen -d /usr/lib/mecab/dic/mecab-ipadic-neologd")

    def wakati(self, ja_str):
        """
        :param str ja_str:
        :rtype: list
        """
        if self.wakati_type == 'mecab-noun':
            wakati_list = self.wakati_mecab(ja_str)
        elif self.wakati_type == 'n-gram':
            wakati_list = self.wakati_ngram(ja_str, self.ngram_n)

        return wakati_list

    def wakati_mecab(self, ja_str):
        """
        :param str ja_str:
        :rtype: str
        """
        self.mt.parse('')

        node = self.mt.parseToNode(ja_str)
        wakati_tokens = []
        while node:
            pos = node.feature.split(',')[0]
            if pos == '名詞':
                wakati_tokens.append(node.surface)
            node = node.next

        return wakati_tokens

    def wakati_ngram(self, ja_str, ngram_n):
        """
        :param str ja_str:
        :param int ngram_n:
        :rtype: str
        """
        self.mt.parse('')

        node = self.mt.parseToNode(ja_str)
        wakati_tokens = []
        while node:
            wakati_tokens.append(node.surface)
            node = node.next

        wakati_ngram = []
        for i in range(len(wakati_tokens)):
            cw = ''
            if i >= self.ngram_n - 1:
                for j in reversed(range(self.ngram_n)):
                    cw += wakati_tokens[i - j]
            else:
                continue
            wakati_ngram.append(cw)

        return wakati_ngram

    def fit(self):
        pass

    def _check_wakati_type(self, wakati_type):

        if not(wakati_type in self.WAKATI_TYPE):
            raise ValueError('You should set wakati_type as "mecab-noun" or "n-gram".')


def concat_all_dataset(root_dir_path, filenames):
    """
    concat all datasets(csv files) to pandas DataFrame
    :param str root_dir_path: root path of dataset directory
    :param list filenames: list of filenames
    :rtype: pandas.DataFrame
    """

    for i, file in enumerate(tqdm(filenames)):
        df = pd.read_csv(os.path.join(root_dir_path, file))
        if i == 0:
            concat_df = df
        else:
            concat_df = pd.concat([concat_df, df])

    return concat_df

if __name__ == '__main__':

    category_choices = CATEGORIES.copy()
    category_choices.append('all')

    parser = argparse.ArgumentParser()
    parser.add_argument('category', choices=category_choices)
    parser.add_argument('--wakati_type', '-w', choices=PreprocessDataset.WAKATI_TYPE, default="mecab-noun")
    parser.add_argument('--ngram_n', '-n', type=int)
    args = parser.parse_args()

    if args.ngram_n:
        preprocess_dataset = PreprocessDataset(args.wakati_type, args.ngram_n)

    else:
        preprocess_dataset = PreprocessDataset(args.wakati_type)

    if args.category == "all":
        files = os.listdir(ROW_DATASET_DIR)
        df = concat_all_dataset(ROW_DATASET_DIR, files)
    else:
        df = pd.read_csv(ROW_DATASET_DIR, args.category + ".csv")

    print("[ PREPROCESS ] Now wakatigaki...")
    df['article'] = df['article'].apply(lambda x: preprocess_dataset.wakati(str(x)))

    if args.wakati_type == "n-gram":
        csv_filename = "{}-gram_{}.csv".format(args.ngram_n, args.category)
    else:
        csv_filename = "{}_{}.csv".format(args.wakati_type, args.category)
    if not os.path.isdir(PREPROCESSED_DATASET_DIR):
        os.makedirs(PREPROCESSED_DATASET_DIR)

    df.to_csv(os.path.join(PREPROCESSED_DATASET_DIR, csv_filename), index=False)
