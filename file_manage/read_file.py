# 这个模块对信息进行读取
import csv


def file_read(file_name):
    """
    这是一个打开文件的函数返回值是生成的数据的列表
    :param file_name: 打开的文件的名字
    """
    with open(file_name, "r", newline='', encoding="utf-8-sig") as f:
        csv_reader = csv.reader(f)
        # print(csv_reader)
        r_list = []
        for row in csv_reader:
            r_list.append(row)
    return r_list


if __name__ in "__main__":
    massages = ['_%f', '对%f的解释', "另一个解释"]
    massages1 = ['_%d', '对%d的解释']
    massages2 = ['_%s', '对%s的解释']
    with open("mode1.csv", 'w', newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(massages)
        csv_writer.writerow(massages1)
        csv_writer.writerow(massages2)

    result = file_read("test.csv")
    for resul in result:
        print(resul)