"""
测试代理IP是否可用？
"""

# -*- coding: utf-8 -*-

import telnetlib

#import aiohttp as aiohttp

from config import *


def test_proxy_vaild(proxy):
    ip, port = proxy.split(":")
    try:
        tn = telnetlib.Telnet(ip, int(port), timeout=20)
    except Exception as e:
        print(e)
        return False
    else:
        return True


if __name__ == '__main__':
    print('ok' if test_proxy_vaild(proxy=input("请输入地址: ")) else 'error')
