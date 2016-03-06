import random

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import metrics
from sklearn.externals import joblib

import numpy

from src import libs


def train_model(user_mat, expected_label, model_output_path, train_part=20):
    user_mat = numpy.array(user_mat)
    expected_label = numpy.array(expected_label)

    # random seq
    seq = random.sample(range(len(user_mat)), len(user_mat) * train_part / 100.0)
    train_mat = [user_mat[i] for i in seq]

    print('start train svm\n')
    # LogisticRegression
    clf = LogisticRegression()
    clf.fit(train_mat, expected_label)
    joblib.dump(clf, model_output_path)

    # test
    predicted_label = list(map(lambda user: clf.predict(libs.generate_user_vec(user, dictionary)), user_mat))

    print(metrics.classification_report(numpy.array(expected_label), numpy.array(predicted_label)))
