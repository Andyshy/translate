# -*- coding:utf-8 -*-
import time
import requests
from urllib.parse import urlencode

"""
金山翻译查询入口
http://www.iciba.com/index.php?
callback=jQuery190034858312023369775_1536974699247&
a=getWordMean&
c=search&
list=1%2C2%2C3%2C4%2C5%2C8%2C9%2C10%2C12%2C13%2C14%2C15%2C18%2C21%2C22%2C24%2C3003%2C3004%2C3005&
word=%E4%BD%A0%E5%A5%BD&
_=1536974699248"""
def get_params(content):
    data = {
        'a': 'getWordMean',
        'c': 'search',
        'list': '1,2,3,4,5,8,9,10,12,13,14,15,18,21,22,24,3003,3004,3005',
        'word': content,
        '_': str(int(time.time() * 1000))
    }
    return data

def get_callback():
    pass


def get_content(url, content):
    data = get_params(content)
    headers = {
        'Host': 'www.iciba.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'http://www.iciba.com/'
    }
    url = url + urlencode(data)
    response = requests.get(url=url, headers = headers)
    results = response.json()
    print(content,":",results.get("baesInfo"))
    print(response.json())


if __name__ == "__main__":
    url = 'http://www.iciba.com/index.php?'
    content = '数据分析师'
    get_content(url=url, content=content)
