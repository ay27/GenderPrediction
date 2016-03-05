# read train data
import random

import jieba
import numpy
from sklearn.externals import joblib
from sklearn.metrics import metrics

from src import libs
from src.DataProcess import DataProcess

dataProc = DataProcess('../data', None, None)
user_list = [user for user in dataProc.get_all_user_obj_with_gender()]


# read from dict file
user_dict = set()
with open('user_dict.txt', 'r') as file:
    for line in file.readline():
        words = line.split()
        user_dict.add(words)
user_dict = list(user_dict)

# user vector
user_mat = []
label = []
count = 0
for user in user_list:
    count += 1
    print(' %d' % count)
    user_mat.append(libs.generate_user_vec(user, user_dict))
    label.append(libs.gender2label(user.gender))
user_mat = numpy.array(user_mat)
label = numpy.array(label)

# load svm model
clf = joblib.load('model/svm.txr')


# test
expected_label = label
predicted_label = [clf.predict(libs.generate_user_vec(user, user_dict)) for user in user_list]

with open('result.txt', 'w') as output:
    output.write(metrics.classification_report(numpy.array(expected_label), numpy.array(predicted_label)))
