import random

import jieba
from sklearn import svm
from sklearn.metrics import metrics
from sklearn.externals import joblib

import numpy

# jieba_test.load_userdict('dict.txt')
from src import libs
from src.DataProcess import DataProcess


jieba.enable_parallel(4)

# read train data
dataProc = DataProcess('../data2', None, None)
user_list = [user for user in dataProc.get_all_user_obj_with_gender()]

# split user data
user_dict = set()
count = 0
with open('user_dict.txt', 'w') as file:
    for user in user_list:
        words = jieba.lcut(user.content, cut_all=False, HMM=True)
        count += 1
        print(count)
        for word in words:
            if len(word) >= 2:
                user_dict.add(word)
                file.write(' %s' % word)

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

# random seq
seq = random.sample(range(len(user_dict)), 1500)
train_mat = [user_mat[i] for i in seq]

print('start train svm\n')
# svm
clf = svm.LinearSVC(C=30, max_iter=500)
clf.fit(train_mat, label)
joblib.dump(clf, 'model/svm.txr')

# test
expected_label = label
predicted_label = [clf.predict(libs.generate_user_vec(user, user_dict)) for user in user_list]

print(metrics.classification_report(numpy.array(expected_label), numpy.array(predicted_label)))


