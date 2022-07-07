# 这是这个任务的命令的控制中心
from manage_message_file import Folder
import json
import post


class Select(object):
    def __init__(self):
        # 初始化一个
        self.folder = Folder()
        try:
            self.folder.get_file_message()
        except Exception as result:
            self.folder.save_file_message()
        self.commend_list = []

    def set_a_cmd(self, cmd, message, num):
        """
        设置一个命令
        @param cmd: 命令
        @param message:命令表示的内容
        @param num: 代表的操作号
        """
        SELECT = {}
        SELECT["cmd"] = cmd
        SELECT["doing"] = num
        SELECT["message"] = message
        for cm in self.commend_list:
            if cm["cmd"] == cmd:
                print("已经有这个命令了")
                return
        self.commend_list.append(SELECT)
        self.save_cmd()

    def get_cmd(self):
        # 得到现在已将有命令(暂时好像没有啥用以后可能会加入自定义命令)
        with open("dictionary\\P_cmd.json", 'r', encoding="utf-8") as f:
            self.commend_list = json.load(f)

    def save_cmd(self):
        # 把命令保存起来
        with open("dictionary\\P_cmd.json", 'w', encoding="utf-8") as f:
            json.dump(self.commend_list, f)

    def select_a_cmd(self, cmd):
        # 寻找一个命令对应的操作
        num = 0
        for lis in self.commend_list:
            if cmd == lis["cmd"]:
                self.run_cmd(num)
                return
            num += 1
        # 收到的不是命令
        file = self.folder.get_file(cmd)
        if file != -1:
            self.deal_file(file)
            return
        else:
            print(f"没有找到相关: {cmd}的信息")
        return

    def run_cmd(self, num):
        if num == 0:
            self.add_new_file(num)
        if num == 1:
            self.del_a_file()
        if num == 2:
            self.dictionary()
        if num == 3:
            self.show_all_cmd()
        if num == 4:
            self.file_super_deal()
        if num == 5:
            self.show_add_file()

    def add_new_file(self, num):
        # 添加文件的命令处理
        print(f"开始运行命令{num}")
        file_name = input("print('请输入你要添加的文件名(有格式名.csv或.txt)：")
        print("请输入你要添加文件的模式")
        print("\t模式1：csv文件， 没有经过处理")
        print("\t模式2：csv文件， 经过上下级的处理")
        print("\t模式3：txt文件， 一行名字一行数据")
        print("\t模式4：txt文件， 每行为一个信息， 通过一个分隔符分为两部分")
        print("\t注：文字应该为utf-8模式")
        file_mode = int(input("你选择的添加模式是: "))
        file_cut = input("请输入文件的缩写：")
        file_cut = file_cut.strip()
        if file_mode == 4:
            file_split = input("请输入文件的分隔符(请区分中英文的符号问题)： ")
        else:
            file_split = ''
        self.folder.add_new_file(file_name, file_mode, file_cut, file_split)

    def del_a_file(self):
        file__name = input("请输入你要删除的文件的名称： ")
        file__name = file__name.strip()
        self.folder.del_file(file__name)

    def dictionary(self):
        post.baidu_dictionary()

    def show_all_cmd(self):
        for cm in self.commend_list:
            print(cm["cmd"] + ": " + cm["message"])
        print("如果输入已经加入的文件名就会进入文件的检索")

    def file_super_deal(self):
        # 对文件进行高级操作
        file_name = input("选择进行操作的文件缩写： ")
        file_name = file_name.strip()
        file_now = self.folder.get_file(file_name)
        if file_now != -1:
            while True:
                # 文件存在
                print("选择进行事件")
                print("\t1.进行添加信息的关系")
                print("\t2.进行删除文件的关系")
                print("\t3.进行文件信息的添加")
                print("\t4.进行文件信息的删减")
                print("\t5.显示所有的文件信息")
                print("\tq.退出")
                choice = input("请输入你的选择：")
                choice = choice.strip()
                # 进行选择
                if choice == '1' or choice == '2':
                    values = []
                    key = input("请输入要进行设置的索引： ")
                    key = key.strip()
                    dirc = input("请输入设置的方向(上:1， 下:2): ")
                    dirc = dirc.strip()
                    while True:
                        value = input("请输入要添加\删除的值(可以设置多个\n直接回车退出)： ")
                        value = value.strip()
                        if value == '':
                            break
                        values.append(value)
                    if choice == '1':
                        file_now.set_relevant(key, dirc, values)
                    else:
                        file_now.remove_relevant(key, dirc, values)
                elif choice == '3':
                    # 进行添加文件
                    key = input("请输入要添加的索引: ")
                    key = key.strip()
                    values = []
                    while True:
                        value = input("请输入要添加的值：")
                        value = value.strip()
                        if value == '':
                            break
                        values.append(value)
                    ups = []
                    downs = []
                    while True:
                        up = input("请输入要添加的上级(可以设置多个\n直接回车退出)：")
                        up = up.strip()
                        if up == '':
                            break
                        ups.append(up)
                    while True:
                        down = input("请输入要添加的下级(可以设置多个\n直接回车退出)：")
                        down = down.strip()
                        if down == '':
                            break
                        downs.append(down)
                    file_now.message_add(key, values, ups, downs)
                elif choice == '4':
                    key = input("请输入要删除的值： ")
                    key = key.strip()
                    file_now.message_del(key)
                elif choice == '5':
                    file_now.message_show_all()
                elif choice == 'q':
                    break
        else:
            print("没有找到相关的文件，可使用‘show’命令查看已有的文件以及缩写")


    def show_add_file(self):
        for fil in self.folder.file_list:
            print("文件的缩写：", fil['short_cut'], f"\t\t文件名：{fil['file']}")

    def deal_file(self, file):
        while True:
            mes = input("请您输入要在文件中查找的信息：")
            if mes == 'q':
                break
            file.message_find_show_one(mes)


if __name__ == '__main__':
    sele = Select()
    sele.set_a_cmd("add", "用来添加一个文件", 0)
    sele.set_a_cmd("del", "用来删除一个文件", 1)
    sele.set_a_cmd("dic", "进入字典", 2)
    sele.set_a_cmd("help", "查看所有的命令", 3)
    sele.set_a_cmd("super", "进行文件的复杂操作", 4)
    sele.set_a_cmd("show", "查看已经存在的文件", 5)
    while True:
        cmd = input("cmd: ")
        if cmd == 'q':
            break
        sele.select_a_cmd(cmd)
