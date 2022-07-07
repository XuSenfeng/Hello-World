# 这是处理一个文件的类
import read_file
import json


class Message_file(object):

    def __init__(self, file_name):
        """
        文件初始化处理。包括处理分析，再储存
        @param file_name: 文件名
        @param mode: 文件现在的模式，默认为没有处理的模式， 模式2为处理过个scv， 模式3未以行为分界的文本
        """
        # 读取文件并且处理
        self.file_name = file_name
        self.message = []
        self.message_deal_over = []

    def add_new_file(self, mode=1, spilt_w=''):
        # 读取最初始的信息
        self.message = read_file.file_read(self.file_name)
        #判断文件读取的方式
        if mode == 1 or mode == 2:
            self.message_deal_mode1(mode)
        elif mode == 3:
            self.message_deal_mode3()
        elif mode == 4:
            self.message_deal_mode4(split_s=spilt_w)
        self.message_save()

    def find_key(self, key):
        """
        找某个数据的位置
        @param key: 找的数据
        @return: 找到返回位置，找不到返回-1
        """
        num = 0
        for dic in self.message_deal_over:
            if dic["key"] == key:
                return num
            num += 1
        if num == len(self.message_deal_over):
            return -1

    # 处理从文件中读取到的数据
    # 处理模式1/2
    # 模式1： csv文件每一行为一填信息，最左侧为key
    # 模式2： csv文件每一行位一份信息，但是根据自定义的文件格式进行处理过了
    def message_deal_mode1(self, mode):
        # 处理称可以扩张的形式
        for mes in self.message:
            # 加入上下级登记的信息
            if mode == 1:
                mes.insert(1, 0)
                mes.insert(1, 0)
            elif mode == 2:
                # 把保存的字符串转化为数字
                mes[1] = int(mes[1])
                mes[2] = int(mes[2])
            DEC = {}
            DEC["key"] = mes[0]
            # 读取上一级的信息
            if mes[1] == 0:
                DEC["up"] = []
            else:
                DEC["up"] = mes[3:(3+mes[1])]
            # 读取下一级的信息
            if mes[2] == 0:
                DEC["down"] = []
            else:
                DEC["down"] = mes[(3+mes[1]):(3+mes[1]+mes[2])]

            DEC["value"] = mes[(3+mes[1]+mes[2]):]
            # 判断是否有已经出现过的信息
            if self.find_key(DEC["key"]) == -1:
                self.message_deal_over.append(DEC)
            else:
                print(f"{DEC['key']}这一条信息已将存在不进行添加")

    def message_deal_mode3(self):
        # 处理模式3
        # 这是txt文件中每两行为一个整体进行读取
        num = 0
        while num < len(self.message)-1:
            DEC={}
            DEC["key"] = self.message[num][0]
            DEC["value"] = []
            DEC["value"].append(self.message[num+1])
            DEC["up"] = []
            DEC["down"] = []
            if self.find_key(DEC["key"]) == -1:
                self.message_deal_over.append(DEC)
            else:
                print(f"{DEC['key']}这一条信息已将存在不进行添加")
            num += 2

    def message_deal_mode4(self, split_s):
        for mes in self.message:
            for m in mes:
                m = m.split(split_s)
                DEC = {}
                DEC["key"] = m[0]
                DEC["value"] = []
                DEC["value"].append(m[1])
                DEC["up"] = []
                DEC["down"] = []
                if self.find_key(DEC["key"]) == -1:
                    self.message_deal_over.append(DEC)
                else:
                    print(f"{DEC['key']}这一条信息已将存在不进行添加")

    def message_add(self, key, value, up=[], down=[]):
        """
        加入一个新的数据
        @param key: 索引
        @param value: 值
        @param up: 关联上级
        @param down: 关联下级
        """
        DEC = {}
        num = self.find_key('key')
        if num != -1:
            print("这个值已将存在了")
            return
        DEC["key"] = key
        # 读取上一级的信息
        DEC["up"] = up
        DEC["down"] = down
        DEC["value"] = value
        self.message_deal_over.append(DEC)
        self.message_save()

    def message_del(self, w_key):
        """
        删除一个数据
        @param w_key: 删除数据的值
        @return:
        """
        choice = input(f"do you really want to del {w_key}?(y/n): ")
        if choice == 'y':
            num = self.find_key(w_key)
            if num >= 0:
                self.message_deal_over.pop(num)
                print("找到了这个数据并已经删除")
                self.message_save()

    @staticmethod
    def __show_one_string(one_mesg):
        """
        显示一个得到的数据
        @param one_mesg: 信息的列表
        """
        print(f"-- {one_mesg['key']} --的含义为： ")
        for val in one_mesg["value"]:
            print("\t\t", val)
        print("\t相关参数")
        if len(one_mesg["up"]) > 0:
            print("\t\t上级: ", end="")
            for up in one_mesg["up"]:
                print(up, end=',')
        if len(one_mesg["down"]) > 0:
            print("\n\t\t下级: ", end='')
            for down in one_mesg["down"]:
                print(down, end=',')
        print("")

    def message_find_show_one(self, key):
        """
        找到并且查找一个数据
        @param key: 查找数据的key
        """
        num = self.find_key(key)
        if num >= 0:
            result = self.message_deal_over[num]
            self.__show_one_string(result)
        else:
            print("没有找到你要的数据")

    def message_show_all(self):
        """
        显示现在的所有数据
        """
        for v in self.message_deal_over:
            self.__show_one_string(v)

    def message_save(self):
        """
        保存现在已经有的数据
        """
        file_name_j = self.file_name.split(".")[0]
        with open('dictionary\\'+file_name_j+".json", 'w+', encoding="utf-8") as f:
            json.dump(self.message_deal_over, f)

    def message_read(self):
        """
        提取现在已经有的数据
        """
        file_name_j = self.file_name.split(".")[0]
        with open('dictionary\\'+file_name_j+".json", 'r', encoding="utf-8") as f:
            self.message_deal_over = json.load(f)

    def set_relevant(self, key, choice, relevant):
        """
        添加一个，或多个相关的属性
        @param key: 属性的缩影
        @param choice: 选择上级或者下级
        @param relevant: 参数
        """
        num = self.find_key(key)
        if num >= 0:
            if choice == '1':
                # 选择的是上级
                for re in relevant:
                    self.message_deal_over[num]["up"].append(re)
                print("添加成功")
                self.message_save()
                return
            elif choice == '2':
                # 选择的是上级
                for re in relevant:
                    self.message_deal_over[num]["down"].append(re)
                print("添加成功")
                self.message_save()
                return
            else:
                print("没有这个等级")
        else:
            print("没有这个值对应的元素")

    def remove_relevant(self, key, choice, relevant):
        """
        移出一个相关的参数
        @param key: 保存参数的索引值
        @param choice: 选择上级还是下级 1：上级 2：下级
        @param relevant: 删除的参数，可以有多个
        """
        num = self.find_key(key)
        if num >= 0:
            if choice == '1':
                # 选择的是上级
                for rel in relevant:
                    if rel in self.message_deal_over[num]["up"]:
                        self.message_deal_over[num]["up"].remove(rel)
                    else:
                        print(f"没有{rel}这个选项")

            elif choice == '2':
                for rel in relevant:
                    if rel in self.message_deal_over[num]["down"]:
                        self.message_deal_over[num]["down"].remove(rel)
                    else:
                        print(f"这一等级没有{rel}这个选项")
            else:
                print("没有这个等级")



if __name__ == '__main__':
    file = Message_file("python.csv")
    file.add_new_file(2)





