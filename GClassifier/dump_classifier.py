# -*- coding: utf-8 -*-

import os
import sys
import argparse
import pickle
import pandas as pd

from ast import literal_eval
from sklearn.preprocessing import LabelEncoder

sys.path.append(os.pardir)
from GClassifier.g_preprocess import PREPROCESSED_DATASET_DIR
from GClassifier.g_classifier import NaiveBayes

if __name__ == '__main__':

    dataset_choices = []
    for file in os.listdir(PREPROCESSED_DATASET_DIR):
        for i, result in enumerate(os.path.splitext(file)):
            if i % 2 == 0:
                dataset_choices.append(result)

    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", choices=dataset_choices)
    parser.add_argument("--out", type=str, default="", help="full path to serialize model.")
    args = parser.parse_args()

    df = pd.read_csv(os.path.join(PREPROCESSED_DATASET_DIR, args.dataset + ".csv"))
    df = df.dropna()

    # print("[ PROCESS ] Encode label to number.")
    # class_le = LabelEncoder()
    # y = class_le.fit_transform(df['category'].values)
    y = df['category'].values
    print("[ PROCESS ] Extract train article contents.")
    X = [literal_eval(x) for x in df['article'].values]

    naive_bayes = NaiveBayes()
    naive_bayes.train(X, y)

    print("[ PROCESS ] Dump trained naive bayes model to pickle file.")
    with open(os.path.join(args.out, "naive_bayes_model.pkl"), "wb") as wf:
        pickle.dump(naive_bayes, wf)
