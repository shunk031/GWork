# -*- coding: utf-8 -*-

import argparse
import os
import pandas as pd

from tqdm import tqdm
from crawl_page import CATEGORIES

DATASET_DIR = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'data')
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath('__file__')), '..', 'GClassifier', 'dataset', 'row')

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('category', choices=CATEGORIES.keys())
    args = parser.parse_args()

    # define category dataset directory
    # ./data/(category name)
    category_dataset_dir = os.path.join(DATASET_DIR, args.category)

    # make single csv file
    files = os.listdir(category_dataset_dir)
    for i, file in enumerate(tqdm(files)):
        df = pd.read_csv(os.path.join(category_dataset_dir, file))
        if i == 0:
            concat_df = df
        else:
            concat_df = pd.concat([concat_df, df])

    # save csv file
    csv_filename = args.category + ".csv"
    concat_df.to_csv(os.path.join(OUTPUT_DIR, csv_filename), index=False)
