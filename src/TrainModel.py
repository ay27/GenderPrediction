import random

from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn import metrics
from sklearn.externals import joblib
import numpy as np


def train_model(user_mat, user_labels, word_dict, model_output_path, train_part=20):
    user_mat = np.array(user_mat)
    user_labels = np.array(user_labels)

    # random seq
    seq = list(random.sample(range(len(user_mat)), int(len(user_mat) * (train_part / 100))))
    train_mat = np.array([user_mat[i] for i in seq])
    train_label = np.array([user_labels[i] for i in seq])

    # LogisticRegression
    clf = LogisticRegression()
    clf.fit(train_mat, train_label)
    joblib.dump(clf, model_output_path)

    # test myself
    predicted_label = clf.predict(train_mat)

    print(metrics.classification_report(np.array(train_label), np.array(predicted_label)))
