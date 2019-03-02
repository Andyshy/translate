# -*- coding:utf-8 -*-
import re
import ctypes
from urllib.parse import urlencode
import requests

def get_params(ttk, content):
    tk = get_tk(ttk=ttk, r=content)
    data = {
        'client': 't',
        'sl': 'zh-CN',
        'tl': 'en',
        'hl': 'zh-CN',
        'dt': 'at',
        'dt': 'bd',
        'dt': 'ex',
        'dt': 'ld',
        'dt': 'md',
        'dt': 'qca',
        'dt': 'rw',
        'dt': 'rm',
        'dt': 'ss',
        'dt': 't',
        'ie': 'UTF-8',
        'oe': 'UTF-8',
        'source': 'bh',
        'ssel': '0',
        'tsel': '0',
        'kc': '1',
        'tk':tk,
        'q': content
    }
    return data

def get_ttk():
    # \x3d十六进制编码，解码为=
    # \x27解码为'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    page = requests.get("https://translate.google.cn/", headers=headers)
    pattern = re.compile(r'a\\x3d(.*?);var.*?b\\x3d(.*?);return (.*?)\+', re.S)
    results = re.findall(pattern, page.text)
    #print(results)
    a = int(results[0][0])
    b = int(results[0][1])
    return results[0][2] + '.' + str(a+b)

def get_tk(ttk, r):
    m = int(ttk.split(".")[0])
    s = int(ttk.split(".")[1])
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
                if 55296 == (64512 & A) and v + 1 < len(r) and 56320 == (64512 & ord(r[v + 1])):
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
        p = p
    else:
        p = (2147483647 & p) + 2147483648
    p = p % 1e6
    p = str(int(p)) + "." + str((int(p) ^ m))
    print(p)
    return p

def get_n(p, D):
    t = 0
    while t < len(D) - 2:
        a = D[t + 2]
        if a >= "a":
            a = ord(a[0]) - 87
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


def int_overflow(val):
    maxint = 2147483647
    if not -maxint-1 <=val <=maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint -1
    return val


def unsigned_right_shift(n, i):
    if n < 0:
        n = ctypes.c_uint32(n).value
    if i < 0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)


def get_content(url, content):
    ttk = get_ttk()
    data = get_params(ttk=ttk, content=content)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'referer': 'https://translate.google.cn/'
    }
    url = url + urlencode(data)
    response = requests.get(url,headers=headers)
    print(response.json())


if __name__ == "__main__":
    url = "https://translate.google.cn/translate_a/single?"
    content = "数据分析师"
    get_content(url=url,content=content)
    #get_ttk()