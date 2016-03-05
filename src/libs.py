import jieba
import numpy
from sklearn.metrics import metrics


def dict2vector(dict_data):
    vec = [0 for i in range(10001)]
    for k in dict_data:
        vec[k] = dict_data[k]
    return vec


def gender2label(gender):
    if gender == u'男':
        return 1.0
    elif gender == u'女':
        return -1.0
    else:
        return 0.0


def read_gender(filename='gender.txt'):
    gender = []
    with open(filename, 'r') as file:
        for g in file.readlines():
            if u'男' in g:
                gender.append(1.0)
            elif u'女' in g:
                gender.append(-1.0)
    return gender


def report(str, count, accuracy, expected, predicted):
    with open('result/%s.log' % str, 'w') as file:
        file.write('===================\n')
        file.write(str)
        file.write('\ntest result:\n')
        file.write('test case count = %d, accuracy count = %d\n' % (count, accuracy))
        file.write('classification report:\n')
        file.write(metrics.classification_report(numpy.array(expected), numpy.array(predicted)))
        file.write('\n===================\n')


def generate_user_vec(user, dict):
    user_vec = [0 for i in range(len(dict)+1)]
    for word in jieba.lcut(user.content):
        if len(word) >= 2 and word in dict:
            user_vec[dict.index(word)] += 1
    return user_vec