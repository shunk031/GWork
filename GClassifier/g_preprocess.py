# -*- coding: utf-8 -*-

import argparse
import os
import pandas as pd

DATASET_ROOT_DIR = os.path.join(os.path.dirname(os.path.realpath('__file__')), 'dataset')
ROW_DATASET_DIR = os.path.join(DATASET_ROOT_DIR, 'row')
PREPROCESSED_DATASET_DIR = os.path.join(DATASET_ROOT_DIR, 'preprocessed')
CATEGORIES = ["entertainment", "sports", "interesting", "domestic", "overseas", "column", "science", "gourmet"]


class PreprocessDataset:

    def __init__(self):
        pass

if __name__ == '__main__':

    row_datasets = os.listdir(ROW_DATASET_DIR)
    for row_dataset in row_datasets:
        print(row_dataset)
