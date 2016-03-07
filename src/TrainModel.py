import random

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import metrics
from sklearn.externals import joblib
import numpy

from fucking_python_map import async_run
from src import libs


def train_model(user_mat, expected_label, word_dict, model_output_path, train_part=20):
    user_mat = numpy.array(user_mat)
    expected_label = numpy.array(expected_label)

    # random seq
    seq = list(random.sample(range(len(user_mat)), int(len(user_mat) * (train_part / 100))))
    train_mat = [user_mat[i] for i in seq]
    train_label = [expected_label[i] for i in seq]

    print('start train svm\n')
    # LogisticRegression
    clf = LogisticRegression()
    clf.fit(train_mat, train_label)
    joblib.dump(clf, model_output_path)

    # test
    predicted_label = list(async_run(lambda user: clf.predict(user), user_mat))

    print(metrics.classification_report(numpy.array(expected_label), numpy.array(predicted_label)))
