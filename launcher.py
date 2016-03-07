import ast
import os

import jieba

from src.DataProcess import DataProcess
from src.GenerateDict import generate_dict
from src import libs
from src import TrainModel, TestModel

jieba.enable_parallel(4)

# generate dict

train_dirs = 'data/data_s'
dictionary_path = 'model/dictionary.txt'
model_dir = 'model/dump/LogisticRegression.txr'
tmp_user_mat_path = 'model/tmp/user_mat'
tmp_user_label_path = 'model/tmp/label'


def read_file(path):
    with open(path, 'r') as file:
        return ast.literal_eval(file.readline())


if __name__ == '__main__':
    if os.path.isfile(tmp_user_mat_path) and os.path.isfile(tmp_user_label_path) and os.path.isfile(dictionary_path):
        user_mat = read_file(tmp_user_mat_path)
        labels = read_file(tmp_user_label_path)
        raw_dict = read_file(dictionary_path)
    else:
        data_proc = DataProcess(train_dirs, None, None)
        user_raw_data = list(data_proc.get_all_user_obj_with_gender())
        if os.path.isfile(dictionary_path):
            raw_dict = read_file(dictionary_path)
        else:
            raw_dict = generate_dict(user_raw_data)

        user_mat = libs.pack2mat(user_raw_data, raw_dict)
        labels = libs.read_label(user_raw_data)

        libs.dump2file(tmp_user_mat_path, user_mat)
        libs.dump2file(tmp_user_label_path, labels)
        libs.dump2file(dictionary_path, raw_dict)

    print('train')
    TrainModel.train_model(user_mat, labels, raw_dict, model_dir)
    print('test')
    TestModel.test_model(user_mat, labels, raw_dict, model_dir)
