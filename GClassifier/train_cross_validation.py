# -*- coding: utf-8 -*-

import os
import argparse
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from ast import literal_eval
from g_preprocess import PREPROCESSED_DATASET_DIR
from g_classifier import NaiveBayes

if __name__ == '__main__':

    dataset_choices = []
    for file in os.listdir(PREPROCESSED_DATASET_DIR):
        for i, result in enumerate(os.path.splitext(file)):
            if i % 2 == 0:
                dataset_choices.append(result)

    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", choices=dataset_choices)
    parser.add_argument("--kfold", type=int, default=5)
    args = parser.parse_args()

    df = pd.read_csv(os.path.join(PREPROCESSED_DATASET_DIR, args.dataset + ".csv"))
    df = df.dropna()

    print("[ PROCESS ] Encode label to number.")
    class_le = LabelEncoder()
    y = class_le.fit_transform(df['category'].values)
    X = df['article'].values

    ave_accuracy = 0
    print("[ PROCESS ] Start {}-fold Cross validation.".format(args.kfold))
    skf = StratifiedKFold(y, args.kfold)
    for idx, (train_idx, test_idx) in enumerate(skf):
        print("[ PROCESS ] Now {} th validation".format(idx + 1))
        print("[ PROCESS ] Split into train data and test data.")
        X_train, X_test, y_train, y_test = X[train_idx], X[test_idx], y[train_idx], y[test_idx]
        print("{:11} all: {}, train: {}, test: {}".format("", len(X), len(X_train), len(X_test)))

        # extract article contents
        print("[ PROCESS ] Extract train article contents.")
        X_train_doc = [literal_eval(x) for x in X_train]
        X_test_doc = [literal_eval(x) for x in X_test]

        print("[ PROCESS ] Train Naive Bayes Classifler.")
        naive_bayes = NaiveBayes()
        naive_bayes.train(X_train_doc, y_train)
        print("{:11} {}".format("", naive_bayes))
        y_pred = naive_bayes.classify_all(X_test_doc)

        y_true = y_test
        print("[ PROCESS ] {} th Classification report".format(idx + 1))
        print(classification_report(y_true, y_pred))

        print("[ PROCESS ] {} th Confusion Matrix".format(idx + 1))
        print("{}".format(class_le.inverse_transform([x for x in range(8)])))
        print("{}\n".format(confusion_matrix(y_true, y_pred)))

        ave_accuracy += (y_pred == y[test_idx]).sum() / len(y_pred)

    # output average validation score
    print("Average Accuracy: {:.2f} [%]".format((ave_accuracy / args.kfold) * 100))
