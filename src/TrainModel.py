import random

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn import metrics
from sklearn.externals import joblib
import numpy as np


def train_model(user_mat, expected_label, word_dict, model_output_path, train_part=20):
    user_mat = np.array(user_mat)
    expected_label = np.array(expected_label)

    # random seq
    seq = list(random.sample(range(len(user_mat)), int(len(user_mat) * (train_part / 100))))
    train_mat = np.array([user_mat[i] for i in seq])
    train_label = np.array([expected_label[i] for i in seq])

    # LogisticRegression
    clf = LogisticRegression()
    clf.fit(train_mat, train_label)
    joblib.dump(clf, model_output_path)

    # test
    predicted_label = clf.predict(user_mat)

    print(metrics.classification_report(np.array(expected_label), np.array(predicted_label)))
