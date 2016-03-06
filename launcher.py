import jieba

from src.GenerateDict import generate_dict

jieba.enable_parallel(4)

# generate dict

generate_dict('data/data1w/', 'model/user_dict.txt')  # read train data
dataProc = DataProcess(user_raw_data_path, None, None)
raw_user_data = list(dataProc.get_all_user_obj_with_gender())
dictionary = libs.read_dict(dict_path)
user_mat = libs.pack2mat(raw_user_data, dictionary)
expected_label = map(lambda user: libs.gender2label(user.gender), raw_user_data)

# read train data
dataProc = DataProcess(raw_user_data_path, None, None)
user_list = list(dataProc.get_all_user_obj_with_gender())
