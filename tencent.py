# -*- coding:utf-8 -*-
import time
import requests
"""
https://fanyi.qq.com/api/translate
"""


def get_content(url, content):
    #中文译英文，f为zh，t为en
    data = {
        'source': 'auto',
        'target': 'en',
        'sourceText': content,
        'essionUuid': 'translate_uuid' + str(int(time.time() * 1000))
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'fanyi.qq.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Referer': 'https://fanyi.qq.com/'
    }
    response = requests.post(url=url, data=data, headers=headers)
    results = response.json()
    print(results)

if __name__ == "__main__":
    url = 'https://fanyi.qq.com/api/translate'
    content = '来我家吧'
    get_content(url=url, content=content)