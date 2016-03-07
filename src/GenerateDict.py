import jieba
import arff
import os

from fucking_python_map import async_run
from src import libs


def _generate_att_list(count):
    tmp = list(async_run(lambda ii: ('attr%d' % ii, 'REAL'), range(count)))
    tmp.append(('label', ['1.0', '-1.0']))
    return tmp


def _generate_raw_dict(user_list):
    user_dict = {}
    for user in user_list:
        words = jieba.lcut(user.content, cut_all=False, HMM=True)
        words = set(words)
        for word in words:
            if len(word) >= 2:
                if word in user_dict.keys():
                    user_dict[word] += 1
                else:
                    user_dict[word] = 1
    return list(filter(lambda key: user_dict[key] > 1, user_dict))


def _select_feature(raw_dict, user_mat):
    # write to arff file
    obj = {}
    obj['relation'] = 'dictionary'
    obj['attributes'] = _generate_att_list(len(raw_dict))
    obj['data'] = user_mat
    print('attr len %d' % len(obj['attributes']))

    arff_file = open('.tmp.arff', 'w')

    arff.dump(obj, arff_file)

    # use weka to select feature
    ll = os.popen('java -jar FeatureSelect/out/artifacts/FeatureSelect_jar/FeatureSelect.jar .tmp.arff').read()
    os.remove('.tmp.arff')
    selected_index = ll.split()
    return list(async_run(lambda index: raw_dict[int(index)], selected_index))


def generate_dict(user_raw_data):
    raw_dict = _generate_raw_dict(user_raw_data)
    raw_user_mat = libs.pack2mat(user_raw_data, raw_dict)
    return _select_feature(raw_dict, raw_user_mat)
