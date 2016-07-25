import ast

import jieba
from fucking_python_map import fucking_map

place = []
with open('data/place.txt') as f:
    for row in f:
        row = row.split()
        place.append([row[0], int(row[1])])


def gender2label(gender):
    for row in place:
        if gender in row[0]:
            return row[1]
    return 0


# 将用户的评论文本分词,然后根据词典生成向量.此处对词的长度做了限制,唯有当词长至少为2时才记录
def generate_user_vec(user, raw_dict):
    user_vec = [0 for i in range(len(raw_dict))]
    for word in jieba.lcut(user.content):
        if len(word) >= 2 and word in raw_dict:
            user_vec[raw_dict.index(word)] += 1
    return user_vec


# 将从文件中读入的raw data并行地,根据词典转换成向量
def pack2mat(user_list, raw_dict):
    return list(fucking_map(lambda user: generate_user_vec(user, raw_dict), user_list))


# 并行地将user_raw_data中的性别数据转换成数值数据
def read_label(user_raw_data):
    return list(fucking_map(lambda user: gender2label(user.gender), user_raw_data))


# 以下这两个函数一一对应
def dump2file(path, data):
    with open(path, 'w', encoding='utf-8') as file:
        file.write(str(data))


def read_file(path):
    with open(path, 'r', encoding='utf-8') as file:
        return ast.literal_eval(file.readline())
