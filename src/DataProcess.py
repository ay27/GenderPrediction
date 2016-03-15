import os

from src.User import User


class DataProcess:
    def __init__(self, source_folder, wordDictFilename, weightofFeaturesFilename):
        self.number_of_user_with_gender = 0
        self.source_folder = source_folder
        self.number_of_user_without_gender = 0
        self.wordDictFilename = wordDictFilename
        self.weightofFeaturesFilename = weightofFeaturesFilename
        self.word_dict = None

    # 新增函数
    def get_all_user_obj_with_gender(self):
        file_list = os.listdir(self.source_folder)
        for filename in file_list:
            with open(r"%s/%s" % (self.source_folder, filename), "r", encoding="utf-8") as input_source:
                for userText in input_source:
                    if len(userText) > 0:
                        userObject = User(userText)
                        if userObject.gender == '' or userObject.gender is None:
                            if 'female' in filename:
                                userObject.gender = u'女'
                            elif 'male' in filename:
                                userObject.gender = u'男'
                        if userObject.gender == u"男" or userObject.gender == u"女":
                            self.number_of_user_with_gender += 1
                            yield userObject
                    else:
                        continue

    def get_all_userObjects_without_genderLabel(self):
        file_list = os.listdir(self.source_folder)
        for filename in file_list:
            with open(r"%s/%s" % (self.source_folder, filename), "r", encoding='urf-8') as input_source:
                for userText in input_source:
                    # userText = userText.encode("utf-8").strip()
                    # userText = unicode(userText.strip(), "utf8")
                    if len(userText) > 0:
                        userObject = User(userText)
                        if userObject.gender != u"男" and userObject.gender != u"女":
                            self.number_of_user_without_gender += 1
                            yield userObject
                    else:
                        continue

    def get_all_userObjects(self):
        file_list = os.listdir(self.source_folder)
        for filename in file_list:
            with open(r"%s/%s" % (self.source_folder, filename), "r", encoding='utf-8') as input_source:
                for userText in input_source:
                    # userText = userText.encode("utf-8").strip()
                    # userText = unicode(userText.strip(), "utf8")
                    if len(userText) > 0:
                        userObject = User(userText)
                        yield userObject
                    else:
                        continue

    def get_wordDict(self):
        if self.word_dict is not None:
            return self.word_dict
        with open(self.wordDictFilename, "r", encoding='utf-8') as inputTexts:
            texts = inputTexts.read()
            texts_list = texts.split("\n")
            key_list = texts_list[0].split(" ")
            value_list = []
            if len(texts_list) > 1:
                value_list = texts_list[1].strip().split(" ")
                value_list = [int(x) for x in value_list]
            self.word_dict = dict(zip(key_list, value_list))

            return self.word_dict

    def get_weightofFeatures(self):
        with open(self.weightofFeaturesFilename, "r", encoding='utf-8') as inputTexts:
            weight_string = inputTexts.read().split(" ")
            weightofFeatures = [float(x) for x in weight_string]
            return weightofFeatures
