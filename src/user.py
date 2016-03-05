import re


class User:
    gender_comp = re.compile(r",\"gender\":\"(.*?)\",")
    nickname_comp = re.compile(r",\"nick_name\":\"(.*?)\",")
    interesting_label_comp = re.compile(r",\"interesting_label\":\"(.*?)\",")
    individual_resume_comp = re.compile(r",\"individual_resume\":\"(.*?)\",")
    feature_label_comp = re.compile(r",\"feature_label\":\"(.*?)\",")
    internet_account_comp = re.compile(r",\"internet_account\":\"(.*?)\",")
    real_name_comp = re.compile(r",\"real_name\":\"(.*?)\",")
    weight_comp = re.compile(r",\"weight\":\"(.*?)\",")
    content_comp = re.compile(r",\"content\":\"(.*?)\",")
    title_comp = re.compile(r",\"title\":\"(.*?)\",")

    def __init__(self, userText):
        userText = "".join(userText.split())
        gender_list = User.gender_comp.findall(userText)
        self.gender = ("".join(gender_list[0])) if (len(gender_list) > 0) else ""
        self.nickname = "".join(set(User.nickname_comp.findall(userText)))
        self.interestingLabel = "".join("".join(set(User.interesting_label_comp.findall(userText))).split())
        self.individualResume = "".join("".join(set(User.individual_resume_comp.findall(userText))).split())
        self.featureLabel = "".join("".join(set(User.feature_label_comp.findall(userText))).split())
        self.internetAccount = "".join(set(User.internet_account_comp.findall(userText)))
        self.realName = "".join(set(User.real_name_comp.findall(userText)))
        self.weight = "".join(set(User.weight_comp.findall(userText)))

        self.content = "".join("$*$".join(User.content_comp.findall(userText)).split())
        self.title = "".join("$*$".join(set(User.title_comp.findall(userText))).split())
