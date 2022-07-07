import requests


def baidu_dictionary():
    # 网址
    url = "https://fanyi.baidu.com/sug"

    while True:
        try:

            s = input("请输入你要翻译的英文(输入q退出):")
            if s == 'q':
                break
            elif s == '':
                continue

            dat = {
                'kw': s
            }

            resp = requests.post(url, data=dat)
            d = resp.json()
            dict(d)
            for v in d['data']:
                print("\t", v['v'])
        except Exception as result:
            continue
    resp.close()



if __name__ == '__main__':

    baidu_dictionary()


