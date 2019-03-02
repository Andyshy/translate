# -*- coding:utf-8 -*-
import requests
"""
金山翻译翻译入口
http://fy.iciba.com/ajax.php?a=fy
"""


def get_content(url, content):
    #中文译英文，f为zh，t为en
    data = {
        'f': 'auto',
        't': 'auto',
        'w': content
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'fy.iciba.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'http://fy.iciba.com/'
    }
    response = requests.post(url=url, data=data, headers=headers)
    results = response.json()
    result = results.get("content")["out"]
    print(content,result)
    print(response.json())

if __name__ == "__main__":
    url = 'http://fy.iciba.com/ajax.php?a=fy'
    content = '来我家吧'
    get_content(url=url, content=content)