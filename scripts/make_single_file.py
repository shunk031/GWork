# -*- coding: utf-8 -*-

import argparse
import os
import sys

sys.path.append(os.pardir)
from GClassifier.g_preprocess import concat_all_dataset
from GClassifier.g_preprocess import CATEGORIES

DATASET_DIR = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath('__file__')), '..', 'GClassifier', 'dataset', 'row')


def make_single_file(category):
    print("[ PROCESS ] make {} dataset to single csv file.".format(category))

    # define category dataset directory
    # ./data/(category name)
    category_dataset_dir = os.path.join(DATASET_DIR, category)

    # make single csv file
    files = os.listdir(category_dataset_dir)
    # for i, file in enumerate(tqdm(files)):
    #     df = pd.read_csv(os.path.join(category_dataset_dir, file))
    #     if i == 0:
    #         concat_df = df
    #     else:
    #         concat_df = pd.concat([concat_df, df])

    concat_df = concat_all_dataset(category_dataset_dir, files)

    # make row dataset directory if not exists
    try:
        os.makedirs(OUTPUT_DIR)
    except FileExistsError:
        pass

    # save csv file
    csv_filename = category + ".csv"
    concat_df.to_csv(os.path.join(OUTPUT_DIR, csv_filename), index=False)

if __name__ == '__main__':

    category_choices = CATEGORIES.copy()
    category_choices.append("all")

    parser = argparse.ArgumentParser()
    parser.add_argument('category', choices=category_choices)
    args = parser.parse_args()

    if args.category == 'all':
        for category in CATEGORIES:
            make_single_file(category)
    else:
        make_single_file(args.category)
