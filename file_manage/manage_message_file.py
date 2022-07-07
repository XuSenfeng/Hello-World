# 这是一个用于处理文件组的类
import json
from message_file import Message_file


class Folder(object):
    def __init__(self):
        self.file_list = []

    def add_new_file(self, file_name, mode=1, short_cut="", split_s=''):
        # 获取一个文件对象
        # 测试文件是不是可以添加， 如果可以就产生一个对应的文件
        REGISTER = {}
        # 处理文件的缩写
        if short_cut != "":
            REGISTER["short_cut"] = short_cut
        else:
            # 如果没有传入缩写 默认为文件的名字
            s_c = file_name.split(".")[0]
            REGISTER["short_cut"] = s_c
        if self.find_file(REGISTER["short_cut"]) != -1:
            print("你要添加的文件名缩写已将存在, 无法继续添加文件")
            return
        num = self.file_real_name_yn(file_name)
        if num == -1:
            try:
                file = Message_file(file_name)
                file.add_new_file(mode=mode, spilt_w=split_s)
            except Exception as result:
                print("文件初始化出错， 请检查您的参数设置")
                return
        else:
            print(f"文件已经存在了，他的缩写是:{self.file_list[num]['short_cut']}")
            print("如果想更新文件信息请把这一条信息删除，并把对应的json文件删除")

        REGISTER["file"] = file_name
        self.file_list.append(REGISTER)
        self.save_file_message()

    def file_real_name_yn(self, name):
        # 判断一个文件是不是已经有了
        num = 0
        for file in self.file_list:
            if name == file["file"]:
                return num
            num += 1
        return -1


    def get_file_message(self):
        with open("dictionary\\P_file_message.json", 'r', encoding="utf-8") as f:
            self.file_list = json.load(f)

    def save_file_message(self):
        with open("dictionary\\P_file_message.json", 'w+', encoding="utf-8") as f:
            json.dump(self.file_list, f)

    def find_file(self, name):
        """
        在这里根据名字查找一个文件
        @param name: 文件的名字
        @return: 返回文件在列表中的名字 如果没有找到返回0
        """
        num = 0
        for file in self.file_list:
            if file["short_cut"] == name:
                return num
            num += 1
        return -1

    def del_file(self, name):
        # TODO 这里是一个删除一个文件的函数
        num = self.find_file(name)
        if num >= 0:
            choice = input("你真的打算删除这一条信息吗(y/n)： ")
            if choice == 'y':
                self.file_list.pop(num)
                self.save_file_message()
            else:
                return
        else:
            print("没有找到您需要的文件")

    def get_file(self, cut_name):
        num = self.find_file(cut_name)
        if num >= 0:
            file_name = self.file_list[num]["file"]
            file_result = Message_file(file_name)
            # 对文件进行挂载
            file_result.message_read()
            return file_result
        else:
            return -1


if __name__ == '__main__':
    folder = Folder()
    folder.get_file_message()
    print(folder.file_list)
    folder.add_new_file("python.csv", mode=2, short_cut="p2", split_s='')
    file = folder.get_file("m4")
    file.message_show_all()

