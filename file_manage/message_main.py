# 这是处理总信息的一个类
from select_cmd import Select


class Massage_main(object):

    def __init__(self):
        # 初始化文件列表
        self.sele = Select()
        try:
            self.sele.get_cmd()
        except Exception as result:
            self.sele.set_a_cmd("add", "用来添加一个文件", 0)
            self.sele.set_a_cmd("del", "用来删除一个文件", 1)
            self.sele.set_a_cmd("dic", "进入字典", 2)
            self.sele.set_a_cmd("help", "查看所有的命令", 3)
            self.sele.set_a_cmd("super", "进行文件的复杂操作", 4)
            self.sele.set_a_cmd("show", "查看已经存在的文件", 5)
            print("初始化命令完成")
        print("*******可以使用的命令*******")
        self.sele.show_all_cmd()
        print("******注：在所有模式中退出均为 : q ******")

    def Message_main(self):

        while True:
            try:
                cmd = input("cmd> ")
                cmd = cmd.strip()
                if cmd == 'q':
                    break
                self.sele.select_a_cmd(cmd)
            except Exception as result:
                pass

if __name__ == '__main__':
    my_main = Massage_main()
    my_main.Message_main()