import numpy
from sklearn.externals import joblib
from sklearn import metrics


def test_model(user_mat, expected_label, word_dict, model_path):
    user_mat = numpy.array(user_mat)
    expected_label = numpy.array(expected_label)

    # load svm model
    clf = joblib.load(model_path)

    # test
    predicted_label = clf.predict(user_mat)

    print(metrics.classification_report(numpy.array(expected_label), numpy.array(predicted_label)))
