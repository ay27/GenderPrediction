import ast
import os
import jieba
import multiprocessing as mp
from src.DataProcess import DataProcess
from src.GenerateDict import generate_dict
from src import libs
from src import TrainModel, TestModel
import platform

WIN = 0
LINUX = 1
Darwin = 2

if "Windows" in platform.platform():
    SYS_VER = WIN
elif "Darwin" in platform.platform():
    SYS_VER = Darwin
else:
    SYS_VER = LINUX

if SYS_VER != WIN:
    jieba.enable_parallel(mp.cpu_count())

# generate dict

train_dirs = 'data/home_place'
dictionary_path = 'model/dictionary.txt'
model_dir = 'model/dump/LogisticRegression.txr'
tmp_user_mat_path = 'model/tmp/user_mat'
tmp_user_label_path = 'model/tmp/label'

# 整个代码的逻辑是:
# 先将文本的raw数据转换为可以处理的矩阵,然后train,test
if __name__ == '__main__':
    # 判断是否已存在某些处理过的数据,若存在,则直接使用;否则需要重新生成
    if os.path.isfile(tmp_user_mat_path) and os.path.isfile(tmp_user_label_path) and os.path.isfile(dictionary_path):
        user_mat = libs.read_file(tmp_user_mat_path)
        labels = libs.read_file(tmp_user_label_path)
        raw_dict = libs.read_file(dictionary_path)
    else:
        print('without history')
        place = []
        with open('data/place.txt') as f:
            for row in f:
                row = row.split()
                place.append([row[0], int(row[1])])
        data_proc = DataProcess(train_dirs, list(map(lambda row: row[0], place)))
        user_raw_data = list(data_proc.get_all_user_obj_with_place())
        if os.path.isfile(dictionary_path):
            raw_dict = libs.read_file(dictionary_path)
        else:
            raw_dict = generate_dict(user_raw_data)

        user_mat = libs.pack2mat(user_raw_data, raw_dict)
        labels = libs.read_label(user_raw_data)

        # 将生成的数据dump出来,以便下次使用
        libs.dump2file(tmp_user_mat_path, user_mat)
        libs.dump2file(tmp_user_label_path, labels)
        libs.dump2file(dictionary_path, raw_dict)

    print('train')
    TrainModel.train_model(user_mat, labels, raw_dict, model_dir)
    print('test')
    TestModel.test_model(user_mat, labels, raw_dict, model_dir)
