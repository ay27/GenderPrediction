import os

from src.User import User


class DataProcess:
    def __init__(self, source_folder, place_data):
        self.number_of_user_with_gender = 0
        self.source_folder = source_folder
        self.number_of_user_without_gender = 0
        self.place_data = place_data
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

    def get_all_user_obj_with_place(self):
        file_list = os.listdir(self.source_folder)
        cnt = 0
        for filename in file_list:
            with open(r"%s/%s" % (self.source_folder, filename), "r", encoding="utf-8") as input_source:
                for userText in input_source:
                    # if cnt > 1000:
                    #     return
                    if len(userText) > 0:
                        userObject = User(userText)
                        userObject.gender = self.check_place(userObject.gender)
                        if userObject.gender is not None and len(userObject.gender) > 0:
                            cnt += 1
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

    def check_place(self, place):
        for row in self.place_data:
            if row in place:
                return row
        return None
