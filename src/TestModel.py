import numpy
from sklearn.externals import joblib
from sklearn.metrics import metrics

from fucking_python_map import async_run
from src import libs


def test_model(user_mat, expected_label, word_dict, model_path):
    user_mat = numpy.array(user_mat)
    expected_label = numpy.array(expected_label)

    # load svm model
    clf = joblib.load(model_path)

    # test
    predicted_label = list(async_run(lambda user: clf.predict(user), user_mat))

    print(metrics.classification_report(numpy.array(expected_label), numpy.array(predicted_label)))
