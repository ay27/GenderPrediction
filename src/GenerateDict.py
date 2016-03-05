import jieba
import arff
import os

from src import libs
from src.DataProcess import DataProcess


def generate_dict(user_list):
    jieba.enable_parallel(4)

    # split user data
    user_dict = {}
    # count = 0
    # with open('user_dict.txt', 'w') as file:
    for user in user_list:
        words = jieba.lcut(user.content, cut_all=False, HMM=True)
        # count += 1
        # print(count)
        words = set(words)
        for word in words:
            if len(word) >= 2:
                if word in user_dict.keys():
                    user_dict[word] += 1
                else:
                    user_dict[word] = 1
                #         file_name.write(' %s' % word)
    tmp = []
    dict_file = open('dict.txt', 'w')
    for key in user_dict.keys():
        if user_dict[key] > 1:
            tmp.append(key)
            dict_file.write(' %s' % key)

    return tmp


def generate_att_list(count):
    attrs = []
    for i in range(count):
        attrs.append(('attr%d' % i, 'REAL'))
    attrs.append(('label', ['男', '女']))
    return attrs


if __name__ == '__main__':
    # read train data
    dataProc = DataProcess('../data2', None, None)
    user_list = [user for user in dataProc.get_all_user_obj_with_gender()]

    user_dict = generate_dict(user_list)

    mat = []
    for user in user_list:
        vec = libs.generate_user_vec(user, user_dict)
        vec.append(user.gender)
        mat.append(vec)
    print('vec len %d' % len(mat[0]))

    obj = {}
    obj['relation'] = 'dictionary'
    obj['attributes'] = generate_att_list(len(user_dict)+1)
    obj['data'] = mat
    print('attr len %d' % len(obj['attributes']))

    arff_file = open('test.arff', 'w')

    arff.dump(obj, arff_file)

    ll = os.popen('java -jar gender.jar test.arff').read()
    selected_index = ll.split()

    with open('user_dict.txt', 'w') as file:
        for index in selected_index:
            file.write(' %s' % user_dict[int(index)])
