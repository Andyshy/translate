# -*- coding:utf-8 -*-
import re
import json
import requests
import urllib
from urllib.parse import urlencode
from utils import unsigned_right_shift


def get_token_gtk():
    """要携带cookie才能得到正确的token和gtk"""
    url = 'https://fanyi.baidu.com/'
    headers = {
        'Cookie': 'BAIDUID=5DCFD8C8D600C1584B2D0E694A32B088:FG=1; BIDUPSID=5DCFD8C8D600C1584B2D0E694A32B088; PSTM=1533353376; BDUSS=0F3VmRQNVBreG5zNVhWazJMd2dNU0psNDU0MGhsV0RMSkJQazBQamRSLUdjNDViQVFBQUFBJCQAAAAAAAAAAAEAAABVkvxq0e7Qocussb~LwMHLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIbmZluG5mZbM; H_PS_PSSID=1454_21100_26350_22160; PSINO=1; locale=zh; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1535867434,1535867675; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1535867675; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D',
        'Host': 'fanyi.baidu.com',
        'Origin': 'https://fanyi.baidu.com',
        'Referer': 'https://fanyi.baidu.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    response =requests.get(url,headers=headers)
    gtk_pattern = re.compile(r"window.gtk = '(.*?)';", re.S)
    gtk_results = re.findall(gtk_pattern,response.text)
    gtk = gtk_results[0]

    token_pattern = re.compile(r"token:(.*?),", re.S)
    token_results = re.findall(token_pattern, response.text)
    token = token_results[0].replace("'","")
    print(token, gtk)
    return token, gtk

def get_sign(gtk,r):
    m = int(gtk.split(".")[0])
    s = int(gtk.split(".")[1])
    S = {}
    v = 0
    c = 0
    while v < len(r):
        A = ord(r[v])
        if 128 > A:
            S[str(c)] = A
            c = c + 1
        else:
            if 2048 > A:
                S[str(c)] = A >> 6 | 192
                c = c + 1
            else:
                if 55296 == (64512 & A) and v + 1 < len(r) and 56320 == (64512 & ord(r[v+1])):
                    v = v + 1
                    A = 65536 + ((1023 & A) << 10) + (1023 & ord(r[v]))
                    S[str(c)] = A >> 18 | 240
                    c = c + 1
                    S[str(c)] = A >> 12 & 63 | 128
                    c = c + 1
                else:
                    S[str(c)] = A >> 12 | 224
                    c = c + 1
                    S[str(c)] = A >> 6 & 63 | 128
                    c = c + 1
                    S[str(c)] = 63 & A | 128
                    c = c + 1
        v = v + 1
    p = m
    b = 0
    F = "+-a^+6"
    D = "+-3^+b+-f"
    while b < len(S):
        p = p + S[str(b)]
        p = get_n(p, F)
        b = b + 1
    p = get_n(p, D)
    p ^= s
    if not 0 > p:
        p=p
    else:
        p = (2147483647 & p) + 2147483648
    p = p % 1e6
    p = str(int(p)) + "." + str((int(p) ^ m))
    print(p)
    return p


def get_n(p, D):
    t = 0
    while t < len(D)-2:
        a = D[t+2]
        if a >= "a":
            a = ord(a[0])-87
        else:
            a = int(a)
        if D[t + 1] == "+":
            a = unsigned_right_shift(p, a)
        else:
            a = p << a
        if D[t] == "+":
            p = p + a & 4294967295
        else:
            p = p ^ a
        t = t + 3
    return p

def baidu_api(content):
    token, gtk = get_token_gtk()
    url = 'https://fanyi.baidu.com/transapi'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '136',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'BAIDUID=5DCFD8C8D600C1584B2D0E694A32B088:FG=1; BIDUPSID=5DCFD8C8D600C1584B2D0E694A32B088; PSTM=1533353376; BDUSS=0F3VmRQNVBreG5zNVhWazJMd2dNU0psNDU0MGhsV0RMSkJQazBQamRSLUdjNDViQVFBQUFBJCQAAAAAAAAAAAEAAABVkvxq0e7Qocussb~LwMHLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIbmZluG5mZbM; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; locale=zh; PSINO=1; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1536462261,1536462274,1536463260,1536464141; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1536464141; H_PS_PSSID=1454_21100_26350_22160; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D; from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D',
        'Host': 'fanyi.baidu.com',
        'Origin': 'https://fanyi.baidu.com',
        'Referer': 'https://fanyi.baidu.com/?aldtype=16047',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    data = {
        'from': 'zh',
        'to': 'en',
        'query': content,
        'transtype':'translang',
        'simple_means_flag': '3',
        'sign': str(get_sign(gtk=gtk,r=content)),
        'token': str(token)
    }
    data = bytes(urlencode(data), encoding='utf-8')
    req = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
    response = urllib.request.urlopen(req)
    response = response.read().decode('utf-8')
    print(json.loads(response))




if __name__=="__main__":
    baidu_api("我爱你")
    #get_token_gtk()

