import copy

import jieba
import arff
import os

from fucking_python_map import fucking_map
from src import libs


# 生成符合arff文件格式的attribute序列
def _generate_att_list(count):
    tmp = list(fucking_map(lambda ii: ('attr%d' % ii, 'REAL'), range(count)))
    tmp.append(('label', ['1.0', '-1.0']))
    return tmp


# 根据所有的训练数据生成词典.当词长至少为2时才记录,免去了大量的单字词语;同时将出现次数小于2的词删去
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
    return list(filter(lambda key: user_dict[key] > 10, user_dict))


# 调用使用weka库编写的特征选择方法,筛选优秀的特征
def _select_feature(raw_dict, labels, user_mat):
    # write to arff file
    obj = {}
    obj['relation'] = 'dictionary'
    obj['attributes'] = _generate_att_list(len(raw_dict))
    concat_user_mat = copy.deepcopy(user_mat)
    for ii in range(len(concat_user_mat)):
        concat_user_mat[ii].append(labels[ii])
    obj['data'] = concat_user_mat

    arff_file = open('.tmp.arff', 'w', encoding='utf-8')
    arff.dump(obj, arff_file)

    # use weka to select feature
    ll = os.popen('java -jar FeatureSelect/out/artifacts/FeatureSelect_jar/FeatureSelect.jar .tmp.arff').read()
    # os.remove('.tmp.arff')
    selected_index = ll.split()
    return list(fucking_map(lambda index: raw_dict[int(index)], selected_index))


# 对外提供的函数,根据raw用户数据生成经过特征选择的词典
def generate_dict(user_raw_data):
    raw_dict = _generate_raw_dict(user_raw_data)
    raw_user_mat = libs.pack2mat(user_raw_data, raw_dict)
    labels = libs.read_label(user_raw_data)
    return _select_feature(raw_dict, labels, raw_user_mat)
