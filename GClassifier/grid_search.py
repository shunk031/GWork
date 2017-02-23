# -*- coding: utf-8 -*-

import argparse
import os
import pandas as pd

from g_preprocess import PREPROCESSED_DATASET_DIR


from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn import svm
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report

if __name__ == '__main__':

    dataset_choices = []
    for file in os.listdir(PREPROCESSED_DATASET_DIR):
        for i, result in enumerate(os.path.splitext(file)):
            if i % 2 == 0:
                dataset_choices.append(result)

    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", choices=dataset_choices)
    parser.add_argument("--loaderjob", type=int, default=1)
    args = parser.parse_args()

    # Load wakatigakied dataset
    df = pd.read_csv(os.path.join(PREPROCESSED_DATASET_DIR, args.dataset + ".csv"))

    # check if NaN is included
    # print(df[df.isnull().any(axis=1)])

    # remove data containing Nan
    df = df.dropna()

    # encode label to number
    class_le = LabelEncoder()
    y = class_le.fit_transform(df['category'].values)
    # extract article contents
    X = df['article'].values

    # split into train data and test data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    count_vec = CountVectorizer()
    X_train_count = count_vec.fit_transform(X_train)
    X_test_count = count_vec.transform(X_test)

    # setting of hyper parameter tuned by grid search
    svm_tuned_parameters = [
        {
            'kernel': ['rbf'],
            'gamma': [2**n for n in range(-15, 3)],
            'C': [2**n for n in range(-5, 15)]
        }
    ]

    scores = ['accuracy']
    for score in scores:
        print('\n' + '=' * 50)
        print(score)
        print('=' * 50)

        clf = GridSearchCV(svm.SVC(), svm_tuned_parameters, cv=5, scoring=score, n_jobs=args.loaderjob)
        clf.fit(X_train_count, y_train)

        print("\n+ ベストパラメータ:\n")
        print(clf.best_estimator_)

        print("\n+ トレーニングデータでCVした時の平均スコア:\n")
        for params, mean_score, all_scores in clf.grid_scores_:
            print("{:.3f} (+/- {:.3f}) for {}".format(mean_score, all_scores.std() / 2, params))

        print("\n+ テストデータでの識別結果:\n")
        y_true, y_pred = y_test, clf.predict(X_test_count)
        print(classification_report(y_true, y_pred))
